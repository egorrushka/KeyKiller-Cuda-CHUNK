// main.cpp
// =============================================================================
//
//  KeyKiller-Cuda-CHUNK
//  https://github.com/egorrushka/KeyKiller-Cuda-CHUNK
//
//  Copyright (C) 2025  egorrushka
//
//  This file is a modified version of main.cpp from:
//    KeyKiller-Cuda  —  https://github.com/Qalander/KeyKiller-Cuda
//    Original algorithm based on VanitySearch by Jean-Luc Pons
//      https://github.com/JeanLucPons/VanitySearch
//
//  All original source code is preserved without modification.
//
//  Modifications made by egorrushka:
//    - Added flag  -s <hex>  : chunk start address
//    - Added flag  -e <hex>  : chunk end address
//    - Added function parseHex() for 256-bit hex parsing
//    - Original -r <bits> mode is fully preserved and unchanged
//
//  This program is free software: you can redistribute it and/or modify
//  it under the terms of the GNU Affero General Public License as published
//  by the Free Software Foundation, either version 3 of the License, or
//  (at your option) any later version.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
//  See the GNU Affero General Public License for more details.
//
//  You should have received a copy of the GNU Affero General Public License
//  along with this program. If not, see <https://www.gnu.org/licenses/>.
//
// =============================================================================

#include <sstream> 
#include "Timer.h"
#include "Vanity.h"
#include "SECP256k1.h"
#include <fstream>
#include <string>
#include <string.h>
#include <stdexcept>
#include <thread>
#include <atomic>
#include <iostream>
#include <vector>
#include <csignal>
#include <cctype>
#include <cuda_runtime.h> 

#if defined(_WIN32) || defined(_WIN64)
#include <conio.h>
#else
#include <termios.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdlib.h>
#endif

// ---------- globals ----------------------------------------------------------
std::atomic<bool> Pause(false);
std::atomic<bool> Paused(false);
std::atomic<bool> stopMonitorKey(false);
int idxcount = 0;
double t_Paused = 0.0;
bool randomMode = false;
bool backupMode = false;

using namespace std;

VanitySearch* g_vanity_search_ptr = nullptr;
std::atomic<bool> g_shutdown_initiated(false);

// ---------- signal handler ---------------------------------------------------
void signalHandler(int signum) {
    if (!backupMode) { printf("\n"); fflush(stdout); exit(signum); }
    if (g_shutdown_initiated.exchange(true)) { exit(signum); }
    cout << "\n[!] Ctrl+C Detected. Shutting down gracefully, please wait...";
    cout.flush();
    if (g_vanity_search_ptr != nullptr) g_vanity_search_ptr->endOfSearch = true;
}

// ---------- keyboard monitor -------------------------------------------------
#if defined(_WIN32) || defined(_WIN64)
void monitorKeypress() {
    while (!stopMonitorKey) {
        Timer::SleepMillis(1);
        if (_kbhit()) {
            char ch = _getch();
            if (ch == 'p' || ch == 'P') Pause = !Pause;
        }
    }
}
#else
struct termios original_termios;
bool terminal_mode_changed = false;
void restoreTerminalMode() {
    if (terminal_mode_changed) tcsetattr(STDIN_FILENO, TCSANOW, &original_termios);
}
void setupRawTerminalMode() {
    tcgetattr(STDIN_FILENO, &original_termios);
    terminal_mode_changed = true;
    struct termios new_termios = original_termios;
    new_termios.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &new_termios);
    int flags = fcntl(STDIN_FILENO, F_GETFL, 0);
    fcntl(STDIN_FILENO, F_SETFL, flags | O_NONBLOCK);
}
void monitorKeypress() {
    while (!stopMonitorKey) {
        Timer::SleepMillis(1);
        char ch;
        if (read(STDIN_FILENO, &ch, 1) > 0)
            if (ch == 'p' || ch == 'P') Pause = !Pause;
    }
}
#endif

// ---------- helpers ----------------------------------------------------------
void printHelp() {
    printf("Usage: kk.exe [-a <addr> | -p <pubkey>] [keyspace] [options]\n\n");
    printf("Target (choose one):\n");
    printf("  -a <b58_addr>   Find private key for a P2PKH Bitcoin address.\n");
    printf("  -p <pubkey>     Find private key for a compressed public key (hex).\n\n");
    printf("Keyspace (choose one):\n");
    printf("  -r <bits>       Bit-range mode: search 2^(bits-1) to 2^bits-1\n");
    printf("                  Example: -r 71  searches the full puzzle #71 range.\n");
    printf("  -s <hex>        Chunk start address (hex). Must be used with -e.\n");
    printf("  -e <hex>        Chunk end   address (hex). Must be used with -s.\n");
    printf("                  Example: -s 0x400000000000000000 -e 0x43ffffffffffffff\n\n");
    printf("Options:\n");
    printf("  -R              Random mode.\n");
    printf("  -b              Backup/resume mode (not for random mode).\n");
    printf("  -G <id>         GPU device ID (default 0).\n");
    printf("  -h, --help      This help.\n\n");
    printf("Press 'p' to pause/resume. Ctrl+C for graceful stop.\n");
    exit(0);
}

int getInt(string name, char* v) {
    int r;
    try { r = std::stoi(string(v)); }
    catch (std::invalid_argument&) {
        fprintf(stderr, "[ERROR] Invalid %s argument, number expected\n", name.c_str());
        exit(-1);
    }
    return r;
}

bool loadBackup(int& idxcount, double& t_Paused, int gpuid) {
    string filename = "schedule_gpu" + to_string(gpuid) + ".dat";
    ifstream inFile(filename, std::ios::binary);
    if (inFile) {
        inFile.read(reinterpret_cast<char*>(&idxcount), sizeof(idxcount));
        inFile.read(reinterpret_cast<char*>(&t_Paused), sizeof(t_Paused));
        inFile.close();
        return true;
    }
    return false;
}

// Parse hex string (with or without "0x") into a 256-bit Int.
// Returns false and prints error on failure.
static bool parseHex(const string& raw, Int& out) {
    string s = raw;
    // strip 0x / 0X prefix
    if (s.size() >= 2 && s[0] == '0' && (s[1] == 'x' || s[1] == 'X'))
        s = s.substr(2);
    if (s.empty()) { fprintf(stderr, "[ERROR] Empty hex value.\n"); return false; }
    for (char c : s) {
        if (!isxdigit((unsigned char)c)) {
            fprintf(stderr, "[ERROR] Bad hex char '%c' in '%s'\n", c, raw.c_str());
            return false;
        }
    }
    if (s.size() > 64) { fprintf(stderr, "[ERROR] Hex value >256 bits: '%s'\n", raw.c_str()); return false; }
    // Int::SetBase16 needs exactly 64 chars, padded with leading zeros
    while (s.size() < 64) s.insert(s.begin(), '0');
    vector<char> buf(s.begin(), s.end());
    buf.push_back('\0');
    out.SetBase16(buf.data());
    return true;
}

// ---------- main -------------------------------------------------------------
int main(int argc, char* argv[]) {

    signal(SIGINT, signalHandler);

#if !(defined(_WIN32) || defined(_WIN64))
    atexit(restoreTerminalMode);
    setupRawTerminalMode();
#endif

    std::thread inputThread(monitorKeypress);
    Timer::Init();
    Secp256K1* secp = new Secp256K1();
    secp->Init();

    if (argc < 2) printHelp();

    string target_address;
    string target_pubkey;
    int    bits   = 0;
    int    gpuId  = 0;
    string hexStart;   // -s
    string hexEnd;     // -e
    uint32_t maxFound = 65536 * 4;

    // ---- argument parsing ---------------------------------------------------
    for (int i = 1; i < argc; ++i) {
        string arg = argv[i];
        if (arg == "-h" || arg == "--help") {
            printHelp();
        } else if (arg == "-b") {
            backupMode = true;
        } else if (arg == "-R") {
            randomMode = true;
        } else if (arg == "-a") {
            if (i + 1 < argc) target_address = argv[++i];
            else { fprintf(stderr, "[ERROR] -a requires an address.\n"); exit(-1); }
        } else if (arg == "-p") {
            if (i + 1 < argc) target_pubkey = argv[++i];
            else { fprintf(stderr, "[ERROR] -p requires a public key.\n"); exit(-1); }
        } else if (arg == "-r") {
            if (i + 1 < argc) {
                bits = getInt("-r", argv[++i]);
                if (bits <= 0 || bits > 256) { fprintf(stderr, "[ERROR] -r must be 1..256.\n"); exit(-1); }
            } else { fprintf(stderr, "[ERROR] -r requires a value.\n"); exit(-1); }
        } else if (arg == "-s") {          // NEW: chunk start
            if (i + 1 < argc) hexStart = argv[++i];
            else { fprintf(stderr, "[ERROR] -s requires a hex value.\n"); exit(-1); }
        } else if (arg == "-e") {          // NEW: chunk end
            if (i + 1 < argc) hexEnd = argv[++i];
            else { fprintf(stderr, "[ERROR] -e requires a hex value.\n"); exit(-1); }
        } else if (arg == "-G") {
            if (i + 1 < argc) gpuId = getInt("-G", argv[++i]);
        } else {
            fprintf(stderr, "[ERROR] Unknown parameter: %s\n", arg.c_str());
            printHelp();
        }
    }

    // ---- validation ---------------------------------------------------------
    if (target_address.empty() && target_pubkey.empty()) {
        fprintf(stderr, "[ERROR] Specify target: -a <address> or -p <pubkey>.\n");
        printHelp();
    }
    if (!target_address.empty() && !target_pubkey.empty()) {
        fprintf(stderr, "[ERROR] Cannot use -a and -p together.\n");
        printHelp();
    }
    if (backupMode && randomMode) {
        fprintf(stderr, "[ERROR] -b and -R cannot be combined.\n");
        exit(-1);
    }

    bool useChunk = (!hexStart.empty() || !hexEnd.empty());
    if (useChunk && (hexStart.empty() || hexEnd.empty())) {
        fprintf(stderr, "[ERROR] -s and -e must be used together.\n");
        exit(-1);
    }
    if (!useChunk && bits == 0) {
        fprintf(stderr, "[ERROR] Keyspace required: -r <bits>  OR  -s <hex> -e <hex>\n");
        printHelp();
    }

    // ---- GPU validation (original code) -------------------------------------
    int deviceCount = 0;
    cudaError_t err = cudaGetDeviceCount(&deviceCount);
    if (err != cudaSuccess) {
        fprintf(stderr, "[ERROR] CUDA error: %s\n", cudaGetErrorString(err));
        exit(-1);
    }
    if (deviceCount == 0) { fprintf(stdout, "[INFO] No CUDA GPU detected. Exiting.\n"); exit(0); }
    if (gpuId >= deviceCount || gpuId < 0) {
        fprintf(stdout, "[INFO] Invalid GPU ID %d (available: 0..%d).\n", gpuId, deviceCount - 1);
        exit(0);
    }

    // ---- build keyspace -----------------------------------------------------
    BITCRACK_PARAM bitcrack, *bc;
    bc = &bitcrack;

    if (useChunk) {
        // Chunk mode: explicit start / end from -s and -e
        if (!parseHex(hexStart, bc->ksStart))  exit(-1);
        if (!parseHex(hexEnd,   bc->ksFinish)) exit(-1);
        if (bc->ksStart.IsZero()) {
            fprintf(stderr, "[ERROR] -s must not be zero.\n"); exit(-1);
        }
        if (bc->ksFinish.IsLower(&bc->ksStart)) {
            fprintf(stderr, "[ERROR] -e must be greater than or equal to -s.\n"); exit(-1);
        }
    } else {
        // Original bit-range mode (unchanged)
        bc->ksStart.SetInt32(1);
        if (bits > 1) bc->ksStart.ShiftL(bits - 1);
        bc->ksFinish.SetInt32(1);
        bc->ksFinish.ShiftL(bits);
        bc->ksFinish.SubOne();
    }
    bc->ksNext.Set(&bc->ksStart);

    // ---- backup restore (original code) -------------------------------------
    if (backupMode) {
        if (loadBackup(idxcount, t_Paused, gpuId))
            printf("[+] Backup restored. Batch: %d, Elapsed: %.2f s.\n", idxcount, t_Paused);
        else
            printf("[+] No backup found. Starting from scratch.\n");
    }

    // ---- banner -------------------------------------------------------------
    vector<string> target_vector;
    string search_target_display;
    if (!target_pubkey.empty()) {
        target_vector.push_back(target_pubkey);
        search_target_display = target_pubkey;
    } else {
        target_vector.push_back(target_address);
        search_target_display = target_address;
    }

    printf("[+] KeyKiller v.007\n");
    if (!target_pubkey.empty())
        printf("[+] Search: %s [Public Key]\n",      search_target_display.c_str());
    else
        printf("[+] Search: %s [P2PKH/Compressed]\n", search_target_display.c_str());

    time_t now = time(NULL);
    printf("[+] Start %s", ctime(&now));
    if (randomMode) printf("[+] Random mode\n");

    if (useChunk)
        printf("[+] Mode: CHUNK\n");
    else
        printf("[+] Range (2^%d)\n", bits);

    printf("[+] from : 0x%s\n", bc->ksStart.GetBase16().c_str());
    printf("[+] to   : 0x%s\n", bc->ksFinish.GetBase16().c_str());
    fflush(stdout);

    // ---- launch search (original code, unchanged) ---------------------------
    VanitySearch* v = new VanitySearch(secp, target_vector, SEARCH_COMPRESSED, true, "", maxFound, bc);
    g_vanity_search_ptr = v;
    vector<int> gpuIds    = { gpuId };
    vector<int> gridSizes = { -1, 128 };
    v->Search(gpuIds, gridSizes);

    stopMonitorKey = true;
    if (inputThread.joinable()) inputThread.join();
    printf("\n");
    delete v;
    delete secp;
    return 0;
}
