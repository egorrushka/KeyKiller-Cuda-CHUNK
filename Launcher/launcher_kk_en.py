"""
KeyKiller Launcher
Copyright (C) 2025  egorrushka
https://github.com/egorrushka/KeyKiller-Cuda-CHUNK
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess, threading, os, sys, json, shutil, time
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
#  База пазлов
# ─────────────────────────────────────────────────────────────────────────────
PUZZLES = {
    71:  ("1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU","400000000000000000","7fffffffffffffffff"),
    72:  ("1JTK7s9YVYywfm5XUH7RNhHJH1LshCaRFR","800000000000000000","ffffffffffffffffff"),
    73:  ("12VVRNPi4SJqUTsp6FmqDqY5sGosDtysn4","1000000000000000000","1ffffffffffffffffff"),
    74:  ("1FWGcVDK3JGzCC3WtkYetULPszMaK2Jksv","2000000000000000000","3ffffffffffffffffff"),
    76:  ("1DJh2eHFYQfACPmrvpyWc8MSTYKh7w9eRF","8000000000000000000","fffffffffffffffffff"),
    77:  ("1Bxk4CQdqL9p22JEtDfdXMsng1XacifUtE","10000000000000000000","1fffffffffffffffffff"),
    78:  ("15qF6X51huDjqTmF9BJgxXdt1xcj46Jmhb","20000000000000000000","3fffffffffffffffffff"),
    79:  ("1ARk8HWJMn8js8tQmGUJeQHjSE7KRkn2t8","40000000000000000000","7fffffffffffffffffff"),
    81:  ("15qsCm78whspNQFydGJQk5rexzxTQopnHZ","100000000000000000000","1ffffffffffffffffffff"),
    82:  ("13zYrYhhJxp6Ui1VV7pqa5WDhNWM45ARAC","200000000000000000000","3ffffffffffffffffffff"),
    83:  ("14MdEb4eFcT3MVG5sPFG4jGLuHJSnt1Dk2","400000000000000000000","7ffffffffffffffffffff"),
    84:  ("1CMq3SvFcVEcpLMuuH8PUcNiqsK1oicG2D","800000000000000000000","fffffffffffffffffffff"),
    86:  ("1K3x5L6G57Y494fDqBfrojD28UJv4s5JcK","2000000000000000000000","3fffffffffffffffffffff"),
    87:  ("1PxH3K1Shdjb7gSEoTX7UPDZ6SH4qGPrvq","4000000000000000000000","7fffffffffffffffffffff"),
    88:  ("16AbnZjZZipwHMkYKBSfswGWKDmXHjEpSf","8000000000000000000000","ffffffffffffffffffffff"),
    89:  ("19QciEHbGVNY4hrhfKXmcBBCrJSBZ6TaVt","10000000000000000000000","1ffffffffffffffffffffff"),
    91:  ("1EzVHtmbN4fs4MiNk3ppEnKKhsmXYJ4s74","40000000000000000000000","7ffffffffffffffffffffff"),
    92:  ("1AE8NzzgKE7Yhz7BWtAcAAxiFMbPo82NB5","80000000000000000000000","fffffffffffffffffffffff"),
    93:  ("17Q7tuG2JwFFU9rXVj3uZqRtioH3mx2Jad","100000000000000000000000","1fffffffffffffffffffffff"),
    94:  ("1K6xGMUbs6ZTXBnhw1pippqwK6wjBWtNpL","200000000000000000000000","3fffffffffffffffffffffff"),
    96:  ("15ANYzzCp5BFHcCnVFzXqyibpzgPLWaD8b","800000000000000000000000","ffffffffffffffffffffffff"),
    97:  ("18ywPwj39nGjqBrQJSzZVq2izR12MDpDr8","1000000000000000000000000","1ffffffffffffffffffffffff"),
    98:  ("1CaBVPrwUxbQYYswu32w7Mj4HR4maNoJSX","2000000000000000000000000","3ffffffffffffffffffffffff"),
    99:  ("1JWnE6p6UN7ZJBN7TtcbNDoRcjFtuDWoNL","4000000000000000000000000","7ffffffffffffffffffffffff"),
    101: ("1CKCVdbDJasYmhswB6HKZHEAnNaDpK7W4n","10000000000000000000000000","1fffffffffffffffffffffffff"),
    102: ("1PXv28YxmYMaB8zxrKeZBW8dt2HK7RkRPX","20000000000000000000000000","3fffffffffffffffffffffffff"),
    103: ("1AcAmB6jmtU6AiEcXkmiNE9TNVPsj9DULf","40000000000000000000000000","7fffffffffffffffffffffffff"),
    104: ("1EQJvpsmhazYCcKX5Au6AZmZKRnzarMVZu","80000000000000000000000000","ffffffffffffffffffffffffff"),
    106: ("18KsfuHuzQaBTNLASyj15hy4LuqPUo1FNB","200000000000000000000000000","3ffffffffffffffffffffffffff"),
    107: ("15EJFC5ZTs9nhsdvSUeBXjLAuYq3SWaxTc","400000000000000000000000000","7ffffffffffffffffffffffffff"),
    108: ("1HB1iKUqeffnVsvQsbpC6dNi1XKbyNuqao","800000000000000000000000000","fffffffffffffffffffffffffff"),
    109: ("1GvgAXVCbA8FBjXfWiAms4ytFeJcKsoyhL","1000000000000000000000000000","1fffffffffffffffffffffffffff"),
    111: ("1824ZJQ7nKJ9QFTRBqn7z7dHV5EGpzUpH3","4000000000000000000000000000","7fffffffffffffffffffffffffff"),
    112: ("18A7NA9FTsnJxWgkoFfPAFbQzuQxpRtCos","8000000000000000000000000000","ffffffffffffffffffffffffffff"),
    113: ("1NeGn21dUDDeqFQ63xb2SpgUuXuBLA4WT4","10000000000000000000000000000","1ffffffffffffffffffffffffffff"),
    114: ("174SNxfqpdMGYy5YQcfLbSTK3MRNZEePoy","20000000000000000000000000000","3ffffffffffffffffffffffffffff"),
    116: ("1MnJ6hdhvK37VLmqcdEwqC3iFxyWH2PHUV","80000000000000000000000000000","fffffffffffffffffffffffffffff"),
    117: ("1KNRfGWw7Q9Rmwsc6NT5zsdvEb9M2Wkj5Z","100000000000000000000000000000","1fffffffffffffffffffffffffffff"),
    118: ("1PJZPzvGX19a7twf5HyD2VvNiPdHLzm9F6","200000000000000000000000000000","3fffffffffffffffffffffffffffff"),
    119: ("1GuBBhf61rnvRe4K8zu8vdQB3kHzwFqSy7","400000000000000000000000000000","7fffffffffffffffffffffffffffff"),
    121: ("1GDSuiThEV64c166LUFC9uDcVdGjqkxKyh","1000000000000000000000000000000","1ffffffffffffffffffffffffffffff"),
    122: ("1Me3ASYt5JCTAK2XaC32RMeH34PdprrfDx","2000000000000000000000000000000","3ffffffffffffffffffffffffffffff"),
    123: ("1CdufMQL892A69KXgv6UNBD17ywWqYpKut","4000000000000000000000000000000","7ffffffffffffffffffffffffffffff"),
    124: ("1BkkGsX9ZM6iwL3zbqs7HWBV7SvosR6m8N","8000000000000000000000000000000","fffffffffffffffffffffffffffffff"),
    126: ("1AWCLZAjKbV1P7AHvaPNCKiB7ZWVDMxFiz","20000000000000000000000000000000","3fffffffffffffffffffffffffffffff"),
    127: ("1G6EFyBRU86sThN3SSt3GrHu1sA7w7nzi4","40000000000000000000000000000000","7fffffffffffffffffffffffffffffff"),
    128: ("1MZ2L1gFrCtkkn6DnTT2e4PFUTHw9gNwaj","80000000000000000000000000000000","ffffffffffffffffffffffffffffffff"),
    129: ("1Hz3uv3nNZzBVMXLGadCucgjiCs5W9vaGz","100000000000000000000000000000000","1ffffffffffffffffffffffffffffffff"),
}
PUZZLE_LABELS = [f"Puzzle {n}" for n in sorted(PUZZLES)]

CFG_MAIN     = "kk_config.json"
CFG_HISTORY  = "kk_history.json"
CFG_PROGRESS = "kk_progress.json"
CFG_TEST     = "kk_test_config.json"
FOUND_FILE   = "found.txt"

# ─────────────────────────────────────────────────────────────────────────────
#  Palette
# ─────────────────────────────────────────────────────────────────────────────
BG=       "#080b10"; PANEL=    "#0d1117"; PANEL2=   "#111620"
BORDER=   "#1a2035"; ACCENT=   "#00d4aa"; ACCENT2=  "#00a882"
GREEN=    "#22c55e"; GREEN2=   "#16a34a"; RED=      "#ef4444"
RED2=     "#dc2626"; BLUE=     "#38bdf8"; ORANGE=   "#f97316"
TEXT=     "#c9d1e0"; MUTED=    "#3d4a66"; ENTRY_BG= "#060910"
TRACK_BG= "#0a0e1a"; VISITED_F="#0e2b1a"; VISITED_L="#22c55e"

FMN=("Consolas",9); FMB=("Consolas",9,"bold"); FMM=("Consolas",10,"bold")
FUI=("Segoe UI",9); FUB=("Segoe UI",9,"bold"); FUH=("Segoe UI",8,"bold")

# ─────────────────────────────────────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────────────────────────────────────
def frac2val(f,rs,rt):  return min(rs+int(f*rt), rs+rt)
def val2frac(v,rs,rt):  return max(0.0,min(1.0,(v-rs)/rt)) if rt else 0.0
def phex(s):
    s=s.strip().lstrip("0x").lstrip("0X")
    try:    return int(s,16) if s else None
    except: return None

# ─────────────────────────────────────────────────────────────────────────────
#  RangeSlider
# ─────────────────────────────────────────────────────────────────────────────
class RangeSlider(tk.Canvas):
    PAD=42; TH=8; SW=11; H=116
    _PCT_Y=2; _Y1=18; _Y2=40; _CY=58

    def __init__(self, master, on_change, **kw):
        kw.setdefault("height",self.H); kw.setdefault("bg",PANEL2); kw.setdefault("highlightthickness",0)
        super().__init__(master,**kw)
        self.on_change=on_change; self._lo=0.0; self._hi=1.0
        self._drag=None; self._locked=False; self._lgap=0.0; self._visited=[]
        self.bind("<Configure>",self._draw); self.bind("<ButtonPress-1>",self._press)
        self.bind("<B1-Motion>",self._move); self.bind("<ButtonRelease-1>",lambda e:setattr(self,"_drag",None))
        self.bind("<MouseWheel>",self._wheel)

    def toggle_lock(self):
        self._locked=not self._locked; return self._locked
    def set(self,lo,hi):
        self._lo=max(0.0,min(1.0,lo)); self._hi=max(0.0,min(1.0,hi)); self._draw()
    def get(self): return self._lo,self._hi
    def add_visited(self,lo,hi):
        lo=max(0.0,min(1.0,lo)); hi=max(0.0,min(1.0,hi))
        if hi>lo: self._visited.append((lo,hi)); self._merge(); self._draw()
    def clear_visited(self): self._visited.clear(); self._draw()
    def get_visited(self): return list(self._visited)
    def set_visited(self,lst): self._visited=[tuple(v) for v in lst]; self._merge(); self._draw()

    def _merge(self):
        if not self._visited: return
        s=sorted(self._visited); m=[list(s[0])]
        for lo,hi in s[1:]:
            if lo<=m[-1][1]+1e-9: m[-1][1]=max(m[-1][1],hi)
            else: m.append([lo,hi])
        self._visited=[tuple(x) for x in m]

    def _tx(self): return self.PAD, self.winfo_width()-self.PAD
    def _fx(self,f):
        x0,x1=self._tx(); return x0+f*(x1-x0)
    def _xf(self,x):
        x0,x1=self._tx(); return max(0.0,min(1.0,(x-x0)/(x1-x0)))

    def _draw(self,_=None):
        self.delete("all"); w=self.winfo_width()
        if w<8: return
        x0,x1=self._tx(); cy=self._CY; ht=self.TH
        self.create_rectangle(x0,cy-ht,x1,cy+ht,fill=TRACK_BG,outline=BORDER)
        for vlo,vhi in self._visited:
            vx0=self._fx(vlo); vx1=self._fx(vhi)
            self.create_rectangle(vx0,cy-ht+1,vx1,cy+ht-1,fill=VISITED_F,outline="")
            self.create_line(vx0,cy-ht+1,vx1,cy-ht+1,fill=VISITED_L,width=2)
        lx=self._fx(self._lo); hx=self._fx(self._hi)
        self.create_rectangle(lx,cy-ht,hx,cy+ht,fill=ACCENT,outline="")
        tb=cy+ht+3
        for i in range(101):
            tx=x0+i/100*(x1-x0)
            if i%10==0:
                self.create_line(tx,tb,tx,tb+9,fill=TEXT,width=1)
                self.create_text(tx,tb+11,text=f"{i}%",font=("Consolas",7,"bold"),fill=TEXT,anchor="n")
            elif i%5==0: self.create_line(tx,tb,tx,tb+6,fill=MUTED,width=1)
            else: self.create_line(tx,tb,tx,tb+3,fill=MUTED,width=1)
        self._thumb(hx,BLUE,  f"{self._hi*100:.3f}%","right")
        self._thumb(lx,ACCENT,f"{self._lo*100:.3f}%","left")
        if self._locked:
            mx=(lx+hx)/2
            self.create_text(mx,cy-ht-14,text="🔒",font=("Segoe UI",10),anchor="s",fill=ORANGE)

    def _thumb(self,sx,color,pct,side):
        sw=self.SW; y1=self._Y1; y2=self._Y2; cy=self._CY; ht=self.TH
        self.create_line(sx,y2,sx,cy+ht,fill=color,width=2)
        self.create_rectangle(sx-sw,y1+3,sx+sw,y2,fill=color,outline="")
        self.create_rectangle(sx-sw+2,y1,sx+sw-2,y2,fill=color,outline="")
        self.create_rectangle(sx-sw,y1+3,sx+sw,y2,fill="",outline="#fff",width=1)
        self.create_polygon([sx-6,y2,sx+6,y2,sx,y2+8],fill=color,outline="#fff",width=1)
        mid=(y1+y2)//2
        for dy in(-4,0,4): self.create_line(sx-sw+4,mid+dy,sx+sw-4,mid+dy,fill="#fff",width=1,stipple="gray50")
        tx=(sx-sw-4) if side=="left" else (sx+sw+4)
        anch="ne" if side=="left" else "nw"
        self.create_text(tx+1,self._PCT_Y+1,text=pct,font=("Consolas",9,"bold"),fill="#000",anchor=anch)
        self.create_text(tx,  self._PCT_Y,  text=pct,font=("Consolas",9,"bold"),fill=color,anchor=anch)

    def _nearest(self,x):
        return "lo" if abs(x-self._fx(self._lo))<=abs(x-self._fx(self._hi)) else "hi"
    def _press(self,e): self._drag=self._nearest(e.x); self._lgap=self._hi-self._lo
    def _move(self,e):
        if not self._drag: return
        f=self._xf(e.x)
        if self._locked:
            g=self._lgap
            if self._drag=="lo": self._lo=max(0.0,min(1.0-g,f)); self._hi=self._lo+g
            else:                self._hi=max(g,min(1.0,f));    self._lo=self._hi-g
        else:
            if self._drag=="lo": self._lo=min(f,self._hi)
            else:                self._hi=max(f,self._lo)
        self._draw(); self.on_change(self._lo,self._hi)
    def _wheel(self,e):
        d=(-1 if e.delta>0 else 1)*0.001; n=self._nearest(e.x)
        if n=="lo": self._lo=max(0.0,min(self._hi,self._lo+d))
        else:       self._hi=max(self._lo,min(1.0,self._hi+d))
        self._draw(); self.on_change(self._lo,self._hi)

# ─────────────────────────────────────────────────────────────────────────────
#  Widget helpers
# ─────────────────────────────────────────────────────────────────────────────
def sep(p,color=BORDER,pady=5): tk.Frame(p,bg=color,height=1).pack(fill="x",pady=pady)
def lbl(p,text,font=FUI,fg=MUTED,bg=PANEL,**kw): return tk.Label(p,text=text,font=font,fg=fg,bg=bg,**kw)
def ent(p,font=FMM,bg=ENTRY_BG,fg=TEXT,width=18,hl=ACCENT,**kw):
    return tk.Entry(p,font=font,bg=bg,fg=fg,insertbackground=fg,relief="flat",
                    highlightthickness=1,highlightbackground=BORDER,highlightcolor=hl,width=width,**kw)
def btn(p,text,cmd,bg=ACCENT,fg=BG,abg=ACCENT2,font=FMB,px=14,py=5,**kw):
    b=tk.Button(p,text=text,command=cmd,font=font,fg=fg,bg=bg,
                activebackground=abg,activeforeground=fg,relief="flat",cursor="hand2",padx=px,pady=py,**kw)
    b.bind("<Enter>",lambda e:b.config(bg=abg)); b.bind("<Leave>",lambda e:b.config(bg=bg)); return b
def panel(p,bg=PANEL,bd=BORDER,**kw):
    return tk.Frame(p,bg=bg,highlightthickness=1,highlightbackground=bd,**kw)
def sec_title(p,text,color=ACCENT,bg=PANEL):
    f=tk.Frame(p,bg=bg); f.pack(fill="x",pady=(0,8))
    tk.Frame(f,bg=color,width=3).pack(side="left",fill="y",padx=(0,8))
    tk.Label(f,text=text,font=FUB,fg=color,bg=bg).pack(side="left"); return f

# ─────────────────────────────────────────────────────────────────────────────
#  App
# ─────────────────────────────────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("⬡  KeyKiller Launcher -EN")
        self.configure(bg=BG); self.resizable(True,True); self.minsize(1200,820)

        self._pnum=71
        addr,hs,he=PUZZLES[71]
        self._rs=int(hs,16); self._re=int(he,16); self._rt=self._re-self._rs
        self._clo_val=self._rs; self._chi_val=self._re

        self._process=None; self._running=False; self._found=False
        self._manual_stop=False; self._watch_thd=None
        self._last_lof=None; self._last_hif=None

        self._build_ui()
        self._load_cfg()
        self._load_test_cfg_auto()
        self._load_history()
        self._tick()
        self.protocol("WM_DELETE_WINDOW",self._on_close)

    # ── build UI ──────────────────────────────────────────────────────────────
    def _build_ui(self):
        self._build_slider(self)
        body=tk.Frame(self,bg=BG); body.pack(fill="both",expand=True,padx=8,pady=(0,8))
        left=tk.Frame(body,bg=BG,width=330); left.pack(side="left",fill="y",padx=(0,8)); left.pack_propagate(False)
        self._build_left(left)
        right=tk.Frame(body,bg=BG); right.pack(side="left",fill="both",expand=True)
        self._build_right(right)

    # ── Slider strip ──────────────────────────────────────────────────────────
    def _build_slider(self,parent):
        sp=tk.Frame(parent,bg=PANEL2,highlightthickness=1,highlightbackground=BORDER)
        sp.pack(fill="x",padx=8,pady=(8,4))

        top=tk.Frame(sp,bg=PANEL2); top.pack(fill="x",padx=12,pady=(8,2))
        lbl(top,"SEARCH RANGE",font=FUB,fg=ACCENT,bg=PANEL2).pack(side="left")
        self._lock_btn=btn(top,"🔓 LOCK",self._toggle_lock,bg=BORDER,fg=TEXT,abg=PANEL2,
                           font=("Segoe UI",8,"bold"),px=10,py=3)
        self._lock_btn.pack(side="left",padx=(14,0))

        prow=tk.Frame(top,bg=PANEL2); prow.pack(side="right")
        lbl(prow,"Start %",font=FUH,fg=MUTED,bg=PANEL2).pack(side="left",padx=(0,3))
        self._plo=tk.StringVar(value="0.000")
        elo=ent(prow,textvariable=self._plo,font=("Consolas",9),fg=ACCENT,hl=ACCENT,width=9)
        elo.pack(side="left",ipady=3)
        elo.bind("<Return>",self._apply_pct); elo.bind("<FocusOut>",self._apply_pct)
        lbl(prow,"  End %",font=FUH,fg=MUTED,bg=PANEL2).pack(side="left",padx=(8,3))
        self._phi=tk.StringVar(value="100.000")
        ehi=ent(prow,textvariable=self._phi,font=("Consolas",9),fg=BLUE,hl=BLUE,width=9)
        ehi.pack(side="left",ipady=3)
        ehi.bind("<Return>",self._apply_pct); ehi.bind("<FocusOut>",self._apply_pct)
        btn(prow,"▶ Apply",self._apply_pct,bg=ACCENT,fg=BG,abg=ACCENT2,
            font=("Segoe UI",8,"bold"),px=10,py=3).pack(side="left",padx=(8,0))

        br=tk.Frame(sp,bg=PANEL2); br.pack(fill="x",padx=14)
        self._lbl_lo=lbl(br,"",font=("Consolas",8),fg=MUTED,bg=PANEL2); self._lbl_lo.pack(side="left")
        self._lbl_hi=lbl(br,"",font=("Consolas",8),fg=MUTED,bg=PANEL2); self._lbl_hi.pack(side="right")

        self.slider=RangeSlider(sp,on_change=self._on_slide,bg=PANEL2)
        self.slider.pack(fill="x",padx=6,pady=(2,4))

        br2=tk.Frame(sp,bg=PANEL2); br2.pack(fill="x",padx=14,pady=(0,4))
        btn(br2,"🗑  Clear visited",self._clear_history,
            bg=BORDER,fg=TEXT,abg=PANEL2,font=("Segoe UI",8,"bold"),px=10,py=2).pack(side="left")
        lg=tk.Frame(br2,bg=PANEL2); lg.pack(side="left",padx=(16,0))
        tk.Frame(lg,bg=VISITED_L,width=14,height=7).pack(side="left",pady=2)
        lbl(lg," visited  ",font=("Segoe UI",8),fg=MUTED,bg=PANEL2).pack(side="left")
        tk.Frame(lg,bg=ACCENT,width=14,height=7).pack(side="left",pady=2)
        lbl(lg," current chunk  🔒=together",font=("Segoe UI",8),fg=MUTED,bg=PANEL2).pack(side="left")

        # HEX display row
        hd=tk.Frame(sp,bg=PANEL2); hd.pack(fill="x",padx=14,pady=(0,6))
        lbl(hd,"Chunk  Start: ",font=FMN,fg=MUTED,bg=PANEL2).pack(side="left")
        self._dlo=lbl(hd,"—",font=FMB,fg=ACCENT,bg=PANEL2); self._dlo.pack(side="left")
        lbl(hd,"   End: ",font=FMN,fg=MUTED,bg=PANEL2).pack(side="left")
        self._dhi=lbl(hd,"—",font=FMB,fg=BLUE,bg=PANEL2); self._dhi.pack(side="left")

    # ── Left ──────────────────────────────────────────────────────────────────
    def _build_left(self,parent):
        cv=tk.Canvas(parent,bg=BG,bd=0,highlightthickness=0)
        sb=tk.Scrollbar(parent,orient="vertical",command=cv.yview,bg=PANEL,troughcolor=BG)
        cv.configure(yscrollcommand=sb.set); sb.pack(side="right",fill="y"); cv.pack(side="left",fill="both",expand=True)
        inn=tk.Frame(cv,bg=BG); cw=cv.create_window((0,0),window=inn,anchor="nw")
        inn.bind("<Configure>",lambda e:cv.configure(scrollregion=cv.bbox("all")))
        cv.bind("<Configure>",lambda e:cv.itemconfig(cw,width=e.width))
        # Mousewheel: scroll the left panel, but NOT when the puzzle combobox is open
        def _on_wheel(e):
            # If the combobox dropdown is open (popdown window exists), do nothing
            try:
                focus = str(e.widget)
                if 'combobox' in focus.lower() or 'popdown' in focus.lower():
                    return
                # Also check if any combobox popdown toplevel exists
                for w in cv.winfo_toplevel().winfo_children():
                    if 'popdown' in str(w).lower():
                        return
            except Exception:
                pass
            cv.yview_scroll(int(-e.delta/120), "units")
        cv.bind_all("<MouseWheel>", _on_wheel)
        # Unbind when combobox opens, rebind when it closes
        def _combo_open(e):
            cv.unbind_all("<MouseWheel>")
        def _combo_close(e):
            cv.bind_all("<MouseWheel>", _on_wheel)
        self._combo_open  = _combo_open
        self._combo_close = _combo_close
        self._build_settings(inn)
        sep(inn,BORDER,pady=4)
        self._build_test_block(inn)

    def _build_settings(self,parent):
        p=panel(parent,bd=ACCENT); p.pack(fill="x",pady=(0,6),padx=2)
        inn=tk.Frame(p,bg=PANEL,padx=10,pady=10); inn.pack(fill="x")
        sec_title(inn,"SETTINGS",ACCENT,PANEL)

        # exe
        lbl(inn,"PATH TO kk.exe",font=FUH,fg=MUTED,bg=PANEL).pack(anchor="w")
        er=tk.Frame(inn,bg=PANEL); er.pack(fill="x",pady=(2,10))
        self._exe=tk.StringVar(value="kk.exe")
        ent(er,textvariable=self._exe,width=22,fg=TEXT,hl=ACCENT).pack(side="left",fill="x",expand=True,ipady=4,ipadx=4)
        btn(er,"📂",self._browse_exe,bg=BORDER,fg=TEXT,abg=PANEL2,font=FUB,px=8,py=4).pack(side="left",padx=(4,0))
        sep(inn,BORDER,4)

        # Puzzle selector
        lbl(inn,"SELECT PUZZLE",font=FUH,fg=MUTED,bg=PANEL).pack(anchor="w",pady=(4,2))
        pr=tk.Frame(inn,bg=PANEL); pr.pack(fill="x",pady=(0,4))
        style=ttk.Style(); style.theme_use("clam")
        style.configure("P.TCombobox",fieldbackground=ENTRY_BG,background=PANEL2,
                        foreground=ORANGE,selectbackground=PANEL2,selectforeground=ORANGE,
                        arrowcolor=ORANGE,bordercolor=BORDER)
        style.map("P.TCombobox",fieldbackground=[("readonly",ENTRY_BG)],foreground=[("readonly",ORANGE)])
        self._pvar=tk.StringVar(value="Puzzle 71")
        self._pcombo=ttk.Combobox(pr,textvariable=self._pvar,values=PUZZLE_LABELS,
                                   state="readonly",width=14,font=("Consolas",11,"bold"),style="P.TCombobox")
        self._pcombo.pack(side="left",ipady=4)
        self._pcombo.bind("<<ComboboxSelected>>", self._on_puzzle)
        self._pcombo.bind("<ButtonPress>",   lambda e: getattr(self,"_combo_open",lambda e:None)(e))
        self._pcombo.bind("<FocusOut>",      lambda e: getattr(self,"_combo_close",lambda e:None)(e))
        self._pcombo.bind("<Escape>",        lambda e: getattr(self,"_combo_close",lambda e:None)(e))
        self._bits_lbl=lbl(pr,"bits: 71",font=("Consolas",10,"bold"),fg=ACCENT,bg=PANEL)
        self._bits_lbl.pack(side="left",padx=(12,0))

        lbl(inn,"PUZZLE ADDRESS (auto)",font=FUH,fg=MUTED,bg=PANEL).pack(anchor="w",pady=(6,2))
        self._addr=tk.StringVar()
        ae=ent(inn,textvariable=self._addr,width=36,fg=GREEN,hl=GREEN)
        ae.pack(fill="x",ipady=5,ipadx=5,pady=(0,8))
        sep(inn,BORDER,4)

        # Manual chunk HEX
        lbl(inn,"CHUNK  — manual HEX input",font=FUH,fg=MUTED,bg=PANEL).pack(anchor="w",pady=(4,2))
        cr=tk.Frame(inn,bg=PANEL); cr.pack(fill="x",pady=(0,4))
        for side,attr,lt,color in [("left","_clo","Start",ACCENT),("right","_chi_var","End",BLUE)]:
            w=tk.Frame(cr,bg=PANEL)
            w.pack(side=side,fill="x",expand=True,padx=(0,4) if side=="left" else (4,0))
            lbl(w,lt,font=FUH,fg=MUTED,bg=PANEL).pack(anchor="w")
            var=tk.StringVar(); setattr(self,attr,var)
            e=ent(w,textvariable=var,fg=color,hl=color,width=20)
            e.pack(fill="x",ipady=4,ipadx=3)
            e.bind("<Return>",self._apply_hex); e.bind("<FocusOut>",self._apply_hex)
        btn(inn,"▶ Apply CHUNK",self._apply_hex,bg=ACCENT,fg=BG,abg=ACCENT2,
            font=FUB,px=10,py=4).pack(fill="x",pady=(4,0))
        sep(inn,BORDER,6)

        # Mode
        lbl(inn,"SEARCH MODE",font=FUH,fg=MUTED,bg=PANEL).pack(anchor="w",pady=(4,4))
        mf=tk.Frame(inn,bg=PANEL); mf.pack(fill="x",pady=(0,6))
        self._mode=tk.StringVar(value="sequential")
        tk.Radiobutton(mf,text="📋  Sequential",variable=self._mode,value="sequential",
                       font=FUI,fg=TEXT,bg=PANEL,selectcolor=ENTRY_BG,
                       activebackground=PANEL,cursor="hand2",
                       command=self._on_mode).pack(anchor="w")
        tk.Radiobutton(mf,text="🎲  Random  (-R)",variable=self._mode,value="random",
                       font=FUI,fg=ORANGE,bg=PANEL,selectcolor=ENTRY_BG,
                       activebackground=PANEL,cursor="hand2",
                       command=self._on_mode).pack(anchor="w",pady=(4,0))
        self._seq_note=lbl(inn,"  ↳ прогресс → kk_progress.json\n  ↳ -b включает resume",
                           font=("Segoe UI",8),fg=MUTED,bg=PANEL)
        self._seq_note.pack(anchor="w",pady=(2,0))
        sep(inn,BORDER,4)

        # GPU + backup
        gr=tk.Frame(inn,bg=PANEL); gr.pack(fill="x",pady=(4,4))
        lbl(gr,"GPU ID:",font=FUH,fg=MUTED,bg=PANEL).pack(side="left")
        self._gpu=tk.StringVar(value="0")
        ent(gr,textvariable=self._gpu,width=4,fg=BLUE,hl=BLUE).pack(side="left",ipady=4,ipadx=4,padx=(6,0))
        self._bkp=tk.BooleanVar(value=False)
        tk.Checkbutton(gr,text="  -b  Resume",variable=self._bkp,
                       font=FUI,fg=TEXT,bg=PANEL,selectcolor=ENTRY_BG,
                       activebackground=PANEL,cursor="hand2").pack(side="left",padx=(12,0))
        sep(inn,BORDER,6)

        # Config buttons
        cr2=tk.Frame(inn,bg=PANEL); cr2.pack(fill="x")
        btn(cr2,"💾  Save config",self._save_cfg,bg=BORDER,fg=TEXT,abg=PANEL2,font=FUB,px=10,py=5).pack(side="left")
        btn(cr2,"📂  Load",self._load_cfg_dlg,bg=BORDER,fg=TEXT,abg=PANEL2,font=FUB,px=10,py=5).pack(side="left",padx=(6,0))
        self._cfgl=lbl(inn,"",font=("Segoe UI",8),fg=GREEN,bg=PANEL)
        self._cfgl.pack(anchor="w",pady=(4,0))


    # ── Test block ────────────────────────────────────────────────────────────
    def _build_test_block(self, parent):
        p = panel(parent, bg=PANEL2, bd=RED)
        p.pack(fill="x", pady=(0,6), padx=2)
        inn = tk.Frame(p, bg=PANEL2, padx=10, pady=10)
        inn.pack(fill="x")

        # Title
        tf = tk.Frame(inn, bg=PANEL2); tf.pack(fill="x", pady=(0,8))
        tk.Frame(tf, bg=RED, width=3).pack(side="left", fill="y", padx=(0,8))
        tk.Label(tf, text="TEST BLOCK", font=FUB, fg=RED, bg=PANEL2).pack(side="left")
        tk.Label(tf, text="  — manual input", font=FUI, fg=MUTED, bg=PANEL2).pack(side="left")

        # Address input
        lbl(inn, "ADDRESS (Compressed P2PKH)", font=FUH, fg=MUTED, bg=PANEL2).pack(anchor="w")
        self._t_addr = tk.StringVar()
        ent(inn, textvariable=self._t_addr, width=36,
            bg=ENTRY_BG, fg=RED, hl=RED).pack(fill="x", ipady=4, ipadx=5, pady=(2,8))

        # Start / End HEX
        tr = tk.Frame(inn, bg=PANEL2); tr.pack(fill="x", pady=(0,6))
        for side, attr, lt, color in [
            ("left",  "_t_start", "Start HEX", ORANGE),
            ("right", "_t_end",   "End HEX",   BLUE),
        ]:
            w = tk.Frame(tr, bg=PANEL2)
            w.pack(side=side, fill="x", expand=True,
                   padx=(0,4) if side=="left" else (4,0))
            lbl(w, lt, font=FUH, fg=MUTED, bg=PANEL2).pack(anchor="w")
            var = tk.StringVar()
            setattr(self, attr, var)
            ent(w, textvariable=var, bg=ENTRY_BG, fg=color, hl=color, width=20
                ).pack(fill="x", ipady=4, ipadx=3)

        sep(inn, BORDER, 3)

        # Mode radiobuttons
        lbl(inn, "TEST MODE", font=FUH, fg=MUTED, bg=PANEL2).pack(anchor="w", pady=(4,2))
        mf = tk.Frame(inn, bg=PANEL2); mf.pack(fill="x", pady=(0,6))
        self._t_mode = tk.StringVar(value="sequential")
        tk.Radiobutton(mf,
                       text="📋  Sequential",
                       variable=self._t_mode, value="sequential",
                       font=FUI, fg=TEXT, bg=PANEL2,
                       selectcolor=ENTRY_BG,
                       activebackground=PANEL2, cursor="hand2"
                       ).pack(side="left")
        tk.Radiobutton(mf,
                       text="🎲  Random  (-R)",
                       variable=self._t_mode, value="random",
                       font=FUI, fg=ORANGE, bg=PANEL2,
                       selectcolor=ENTRY_BG,
                       activebackground=PANEL2, cursor="hand2"
                       ).pack(side="left", padx=(16,0))

        sep(inn, BORDER, 3)

        # Buttons row
        br = tk.Frame(inn, bg=PANEL2); br.pack(fill="x", pady=(6,2))
        self._tbtn = btn(br, "▶  RUN TEST", self._start_test,
                         bg=RED, fg="#ffffff", abg=RED2,
                         font=("Consolas", 10, "bold"), px=14, py=6)
        self._tbtn.pack(side="left")

        self._tstop_btn = btn(br, "■  STOP", self._stop_test,
                              bg=BORDER, fg=TEXT, abg=PANEL2,
                              font=FMB, px=10, py=6)
        self._tstop_btn.pack(side="left", padx=(8,0))
        self._tstop_btn.config(state="disabled")

        self._t_status = lbl(br, "", font=FMB, fg=MUTED, bg=PANEL2)
        self._t_status.pack(side="left", padx=(12,0))

        sep(inn, BORDER, 4)

        # Save / load test config row
        cr = tk.Frame(inn, bg=PANEL2); cr.pack(fill="x")
        btn(cr, "💾  Save test config", self._save_test_cfg,
            bg=BORDER, fg=TEXT, abg=PANEL2, font=FUB, px=10, py=4).pack(side="left")
        btn(cr, "📂  Load", self._load_test_cfg_dlg,
            bg=BORDER, fg=TEXT, abg=PANEL2, font=FUB, px=10, py=4).pack(
            side="left", padx=(6,0))
        self._t_cfgl = lbl(inn, "", font=("Segoe UI", 8), fg=GREEN, bg=PANEL2)
        self._t_cfgl.pack(anchor="w", pady=(4,0))

    def _start_test(self):
        if self._running or getattr(self, "_t_running", False):
            return
        exe  = self._exe.get().strip()
        addr = self._t_addr.get().strip()
        s    = self._t_start.get().strip().lstrip("0x").lstrip("0X")
        e    = self._t_end.get().strip().lstrip("0x").lstrip("0X")
        gpu  = self._gpu.get().strip() or "0"

        if not addr: messagebox.showerror("Error", "Enter address for test."); return
        if not s or not e: messagebox.showerror("Error", "Enter Start and End HEX."); return
        import shutil as _sh
        if not os.path.exists(exe) and not _sh.which(exe):
            messagebox.showerror("File not found", f"kk.exe не найден:\n{exe}"); return

        mode_flag = "-R" if getattr(self, "_t_mode", tk.StringVar()).get() == "random" else ""
        cmd = f"{exe} -a {addr} -s 0x{s} -e 0x{e} -G {gpu}"
        if mode_flag:
            cmd += f" {mode_flag}"
        self._t_running = True; self._t_found = False; self._t_manual_stop = False
        self._tbtn.config(state="disabled")
        self._tstop_btn.config(state="normal")
        self._t_status.config(text="● Running...", fg=GREEN)

        self._log("─"*60, "sep")
        self._log("TEST: " + cmd, "cmd")
        self._log("─"*60, "sep")

        cwd = os.path.dirname(os.path.abspath(__file__))
        try:
            wrap = f"TITLE KeyKiller TEST & MODE CON COLS=130 LINES=30 & {cmd} & pause"
            self._t_process = subprocess.Popen(
                ["cmd", "/K", wrap],
                creationflags=subprocess.CREATE_NEW_CONSOLE, cwd=cwd)
        except Exception as ex:
            self._log(f"❌  Error: {ex}", "found")
            self._set_test_stopped(); return

        import threading as _thr
        _thr.Thread(target=self._test_watcher, daemon=True).start()

    def _stop_test(self):
        self._t_manual_stop = True
        proc = getattr(self, "_t_process", None)
        if proc and proc.poll() is None:
            try:
                subprocess.call(["taskkill","/F","/T","/PID",str(proc.pid)],
                                creationflags=subprocess.CREATE_NO_WINDOW)
            except: pass
        self._set_test_stopped()

    def _set_test_stopped(self):
        self._t_running = False
        self._tbtn.config(state="normal")
        self._tstop_btn.config(state="disabled")
        self._t_status.config(text="●  Stopped", fg=MUTED)

    def _test_watcher(self):
        proc    = self._t_process
        sd      = os.path.dirname(os.path.abspath(__file__))
        kf      = os.path.join(sd, FOUND_FILE)
        t_start = time.time()
        try:
            while proc.poll() is None:
                time.sleep(0.5)
                if getattr(self, "_t_manual_stop", False): return
                if os.path.exists(kf):
                    try:
                        if os.path.getmtime(kf) >= t_start:
                            with open(kf, "r", errors="replace") as f:
                                content = f.read().strip()
                            if content:
                                self.after(0, self._handle_test_found, content)
                                return
                    except: pass
        except: pass
        finally:
            rc = proc.returncode if proc.returncode is not None else "?"
            self.after(0, self._log, f"Test finished (code {rc})", "warn")
            self.after(0, self._set_test_stopped)

    def _handle_test_found(self, content):
        if getattr(self, "_t_found", False): return
        self._t_found = True
        self._stop_test()
        sd  = os.path.dirname(os.path.abspath(__file__))
        src_f = os.path.join(sd, FOUND_FILE)
        ts  = __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S")
        dst = os.path.join(sd, f"TEST_FOUND_{ts}.txt")
        import shutil as _sh
        if os.path.exists(src_f): _sh.copy2(src_f, dst)
        self._t_status.config(text="🔑  FOUND!", fg=GREEN)
        self._log("✅  TEST: KEY FOUND! File: " + dst, "found")
        self._log(content, "found")
        self.after(200, lambda: messagebox.showinfo(
            "✅  KEY FOUND!",
            f"{content}\n\nСохранён: {dst}"))



    # ── Test config ────────────────────────────────────────────────────────────
    def _get_test_cfg(self):
        return {
            "t_addr":  self._t_addr.get(),
            "t_start": self._t_start.get(),
            "t_end":   self._t_end.get(),
            "t_mode":  self._t_mode.get(),
        }

    def _apply_test_cfg(self, d):
        self._t_addr.set(d.get("t_addr", ""))
        self._t_start.set(d.get("t_start", ""))
        self._t_end.set(d.get("t_end", ""))
        self._t_mode.set(d.get("t_mode", "sequential"))

    def _save_test_cfg(self):
        try:
            with open(CFG_TEST, "w") as f:
                json.dump(self._get_test_cfg(), f, indent=2)
            self._flash(self._t_cfgl, "✓ Saved")
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def _load_test_cfg_dlg(self):
        path = filedialog.askopenfilename(
            title="Load test config",
            filetypes=[("JSON", "*.json"), ("All", "*.*")])
        if path:
            try:
                with open(path) as f:
                    self._apply_test_cfg(json.load(f))
                self._flash(self._t_cfgl, "✓ Loaded")
            except Exception as ex:
                messagebox.showerror("Error", str(ex))

    def _load_test_cfg_auto(self):
        if not os.path.exists(CFG_TEST): return
        try:
            with open(CFG_TEST) as f:
                self._apply_test_cfg(json.load(f))
        except: pass

    # ── Right ─────────────────────────────────────────────────────────────────
    def _build_right(self,parent):
        ctrl=tk.Frame(parent,bg=BG); ctrl.pack(fill="x",pady=(0,6))
        self._sbtn=btn(ctrl,"▶  START",self._start,bg=GREEN,fg=BG,abg=GREEN2,
                       font=("Consolas",12,"bold"),px=22,py=8)
        self._sbtn.pack(side="left")
        self._xbtn=btn(ctrl,"■ STOP",self._stop,bg=RED,fg="#fff",abg=RED2,
                       font=("Consolas",12,"bold"),px=18,py=8)
        self._xbtn.pack(side="left",padx=(8,0)); self._xbtn.config(state="disabled")
        self._stlbl=lbl(ctrl,"●  Stopped",font=("Consolas",10,"bold"),fg=MUTED,bg=BG)
        self._stlbl.pack(side="left",padx=14)
        btn(ctrl,"📂 folder",self._open_folder,bg=BORDER,fg=TEXT,abg=PANEL2,font=FUB,px=10,py=6).pack(side="right")

        # Stats panel
        sp=panel(parent,bd=BORDER); sp.pack(fill="x",pady=(0,6))
        si=tk.Frame(sp,bg=PANEL,padx=12,pady=8); si.pack(fill="x")
        sec_title(si,"PARAMETERS  /  INFO",ACCENT,PANEL)
        ls=tk.Frame(si,bg=PANEL); ls.pack(fill="x")
        self._i_puz=self._irow(ls,"Puzzle:")
        self._i_adr=self._irow(ls,"Address:")
        self._i_chk=self._irow(ls,"Chunk:")
        self._i_mod=self._irow(ls,"Mode:")
        self._i_cmd=self._irow(ls,"Command:")

        # Log
        pb=panel(parent,bd=BORDER); pb.pack(fill="both",expand=True)
        ph=tk.Frame(pb,bg=PANEL,padx=12,pady=6); ph.pack(fill="x")
        sec_title(ph,"LOG  (kk.exe — in separate CMD window)",ACCENT,PANEL)
        btn(ph,"✕ clear",self._clear_log,bg=BORDER,fg=MUTED,abg=PANEL2,font=FUB,px=10,py=2).pack(side="right")
        lf=tk.Frame(pb,bg=BG); lf.pack(fill="both",expand=True)
        lsb=tk.Scrollbar(lf,orient="vertical",bg=PANEL,troughcolor=BG); lsb.pack(side="right",fill="y")
        self.log=tk.Text(lf,font=("Consolas",9),bg="#04060d",fg=TEXT,insertbackground=TEXT,
                         relief="flat",highlightthickness=0,wrap="word",state="disabled",padx=10,pady=6)
        self.log.configure(yscrollcommand=lsb.set); lsb.configure(command=self.log.yview)
        self.log.pack(side="left",fill="both",expand=True)
        for tag,fg_c,fo in [("ts",MUTED,None),("info",TEXT,None),("found",RED,("Consolas",11,"bold")),
                             ("warn",ORANGE,None),("cmd",BLUE,None),("sep",MUTED,None)]:
            kw={"foreground":fg_c};
            if fo: kw["font"]=fo
            self.log.tag_config(tag,**kw)
        self._refresh()

    def _irow(self,p,text):
        r=tk.Frame(p,bg=PANEL); r.pack(fill="x",pady=1)
        lbl(r,f"{text:<12}",font=FMN,fg=MUTED,bg=PANEL).pack(side="left")
        v=tk.StringVar(); tk.Label(r,textvariable=v,font=FMN,fg=TEXT,bg=PANEL).pack(side="left"); return v
    def _srow(self,p,text):
        r=tk.Frame(p,bg=PANEL); r.pack(fill="x",pady=1)
        lbl(r,f"{text:<10}",font=FMN,fg=MUTED,bg=PANEL).pack(side="left")
        v=tk.StringVar(value="—"); tk.Label(r,textvariable=v,font=FMN,fg=TEXT,bg=PANEL).pack(side="left"); return v

    # ── Puzzle select ─────────────────────────────────────────────────────────
    def _on_puzzle(self,_=None):
        num=int(self._pvar.get().split()[1]); self._apply_puzzle(num)

    def _apply_puzzle(self,num):
        if num not in PUZZLES: return
        self._pnum=num
        addr,hs,he=PUZZLES[num]
        self._rs=int(hs,16); self._re=int(he,16); self._rt=self._re-self._rs
        self._clo_val=self._rs; self._chi_val=self._re
        bits=self._re.bit_length()
        self._pvar.set(f"Puzzle {num}")
        self._bits_lbl.config(text=f"bits: {bits}")
        self._addr.set(addr)
        self._lbl_lo.config(text=f"{hs.upper()}  (0%)")
        self._lbl_hi.config(text=f"(100%)  {he.upper()}")
        self.slider.set(0.0,1.0)
        self._plo.set("0.000"); self._phi.set("100.000")
        self._clo.set(hs.upper()); self._chi_var.set(he.upper())
        self._dlo.config(text=f"0x{hs.upper()}"); self._dhi.config(text=f"0x{he.upper()}")
        if self.slider.get_visited():
            if messagebox.askyesno("Puzzle change","Clear visited range history?"):
                self.slider.clear_visited(); self._save_history()
        self._refresh()

    # ── Chunk sync (единая точка) ─────────────────────────────────────────────
    def _set_chunk(self,lo,hi,src=""):
        lo=max(self._rs,min(self._re,lo)); hi=max(self._rs,min(self._re,hi))
        if lo>=hi: return
        self._clo_val=lo; self._chi_val=hi
        lf=val2frac(lo,self._rs,self._rt); hf=val2frac(hi,self._rs,self._rt)
        if src!="slider": self.slider.set(lf,hf)
        if src!="pct":
            self._plo.set(f"{lf*100:.4f}"); self._phi.set(f"{hf*100:.4f}")
        if src!="hex":
            self._clo.set(f"{lo:X}"); self._chi_var.set(f"{hi:X}")
        self._dlo.config(text=f"0x{lo:X}"); self._dhi.config(text=f"0x{hi:X}")
        self._refresh()

    def _on_slide(self,lf,hf):
        lo=frac2val(lf,self._rs,self._rt); hi=frac2val(hf,self._rs,self._rt)
        self._set_chunk(lo,hi,"slider")

    def _apply_pct(self,_=None):
        try: lp=float(self._plo.get().replace(",",".")); hp=float(self._phi.get().replace(",","."))
        except: return
        lp=max(0.0,min(100.0,lp)); hp=max(0.0,min(100.0,hp))
        if lp>=hp: return
        self._set_chunk(frac2val(lp/100,self._rs,self._rt),frac2val(hp/100,self._rs,self._rt),"pct")

    def _apply_hex(self,_=None):
        lo=phex(self._clo.get()); hi=phex(self._chi_var.get())
        if lo is None or hi is None or lo>=hi: return
        self._set_chunk(lo,hi,"hex")

    def _toggle_lock(self):
        locked=self.slider.toggle_lock()
        if locked: self._lock_btn.config(text="🔒 LOCK  ON",fg=ORANGE,bg=PANEL2)
        else:       self._lock_btn.config(text="🔓 LOCK",fg=TEXT,bg=BORDER)

    def _on_mode(self): self._refresh()

    # ── refresh info ─────────────────────────────────────────────────────────
    def _refresh(self):
        if not hasattr(self,"_i_puz"): return
        clo=getattr(self,"_clo_val",self._rs); chi=getattr(self,"_chi_val",self._re)
        self._i_puz.set(f"#{self._pnum}")
        self._i_adr.set(self._addr.get())
        self._i_chk.set(f"0x{clo:X}  →  0x{chi:X}")
        self._i_mod.set("Random (-R)" if self._mode.get()=="random" else "Sequential")
        cmd=self._build_cmd(); self._i_cmd.set(cmd[:78]+("..." if len(cmd)>78 else ""))

    # ── build cmd ─────────────────────────────────────────────────────────────
    def _build_cmd(self):
        clo=getattr(self,"_clo_val",self._rs); chi=getattr(self,"_chi_val",self._re)
        exe=self._exe.get().strip(); addr=self._addr.get().strip(); gpu=self._gpu.get().strip() or "0"
        parts=[exe,"-a",addr,"-s",f"0x{clo:X}","-e",f"0x{chi:X}","-G",gpu]
        if self._mode.get()=="random": parts.append("-R")
        elif self._bkp.get(): parts.append("-b")
        return " ".join(parts)

    # ── launch ────────────────────────────────────────────────────────────────
    def _start(self):
        if self._running: return
        exe=self._exe.get().strip()
        if not os.path.exists(exe) and not shutil.which(exe):
            messagebox.showerror("File not found",f"kk.exe не найден:\n{exe}"); return
        if not self._addr.get().strip():
            messagebox.showerror("No address","Select a puzzle from the list."); return
        self._running=True; self._found=False; self._manual_stop=False
        self._sbtn.config(state="disabled"); self._xbtn.config(state="normal")
        self._stlbl.config(text="● Starting...",fg=GREEN)
        clo=getattr(self,"_clo_val",self._rs); chi=getattr(self,"_chi_val",self._re)
        self._last_lof=val2frac(clo,self._rs,self._rt)
        self._last_hif=val2frac(chi,self._rs,self._rt)
        cmd=self._build_cmd()
        self._log("─"*60,"sep")
        self._log(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  Started  Puzzle #{self._pnum}","warn")
        self._log("Command: "+cmd,"cmd"); self._log("─"*60,"sep")
        self._save_progress()
        cwd=os.path.dirname(os.path.abspath(__file__))
        try:
            title=f"KeyKiller  Puzzle #{self._pnum}"
            wrap=f"TITLE {title} & MODE CON COLS=160 LINES=40 & {cmd} & pause"
            self._process=subprocess.Popen(["cmd","/K",wrap],
                                            creationflags=subprocess.CREATE_NEW_CONSOLE,cwd=cwd)
        except Exception as ex:
            self._log(f"❌  Error: {ex}","found"); self._set_stopped(); return
        self._watch_thd=threading.Thread(target=self._watcher,daemon=True); self._watch_thd.start()

    def _stop(self):
        self._manual_stop=True
        if self._process and self._process.poll() is None:
            try: subprocess.call(["taskkill","/F","/T","/PID",str(self._process.pid)],
                                  creationflags=subprocess.CREATE_NO_WINDOW)
            except: pass
        self._set_stopped(); self._log("⏹  Stopped manually.","warn")

    def _set_stopped(self):
        self._running=False; self._sbtn.config(state="normal"); self._xbtn.config(state="disabled")
        self._stlbl.config(text="●  Stopped",fg=MUTED)

    def _watcher(self):
        proc=self._process; sd=os.path.dirname(os.path.abspath(__file__))
        kf=os.path.join(sd,FOUND_FILE)
        # Запоминаем время запуска — ищем found.txt изменённый ПОСЛЕ старта
        t_start=time.time()
        try:
            while proc.poll() is None:
                time.sleep(0.8)
                if os.path.exists(kf):
                    try:
                        if os.path.getmtime(kf) >= t_start:
                            with open(kf,"r",errors="replace") as fh: content=fh.read().strip()
                            if content: self.after(0,self._handle_found,content); return
                    except: pass
        except Exception as ex: self.after(0,self._log,f"[watcher] {ex}","warn")
        finally:
            rc=proc.returncode if proc.returncode is not None else "?"
            self.after(0,self._log,f"kk.exe exited (code {rc})","warn")
            if not self._found and not self._manual_stop: self.after(0,self._record_visited)
            self.after(0,self._set_stopped)

    def _handle_found(self,content):
        if self._found: return
        self._found=True; self._stop()
        sd=os.path.dirname(os.path.abspath(__file__))
        src=os.path.join(sd,FOUND_FILE); ts=datetime.now().strftime("%Y%m%d_%H%M%S")
        dst=os.path.join(sd,f"FOUND_{ts}.txt")
        if os.path.exists(src): shutil.copy2(src,dst)
        self._log("\n"+"★"*55,"found"); self._log("  🔑  НАЙДЕН ПРИВАТНЫЙ КЛЮЧ!","found")
        self._log(f"  Сохранён: {dst}","found"); self._log("★"*55,"found"); self._log(content,"found")
        self._record_visited()
        self.after(200,lambda: messagebox.showinfo("🔑  КЛЮЧ НАЙДЕН!",f"Ключ найден!\nСохранён: {dst}"))

    def _tick(self):
        if self._running: self._stlbl.config(text="● Running...",fg=GREEN)
        self.after(500,self._tick)

    # ── history ───────────────────────────────────────────────────────────────
    def _load_history(self):
        if not os.path.exists(CFG_HISTORY): return
        try:
            with open(CFG_HISTORY) as f: d=json.load(f)
            if d.get("puzzle")==self._pnum: self.slider.set_visited(d.get("visited",[]))
        except: pass

    def _save_history(self):
        try:
            with open(CFG_HISTORY,"w") as f:
                json.dump({"puzzle":self._pnum,"visited":self.slider.get_visited()},f,indent=2)
        except: pass

    def _clear_history(self): self.slider.clear_visited(); self._save_history(); self._log("🗑  History cleared.","warn")

    def _record_visited(self):
        if self._last_lof is not None:
            self.slider.add_visited(self._last_lof,self._last_hif); self._save_history()
            self._log(f"✔  {self._last_lof*100:.3f}% – {self._last_hif*100:.3f}%  marked as visited.","info")

    # ── progress ──────────────────────────────────────────────────────────────
    def _save_progress(self):
        clo=getattr(self,"_clo_val",self._rs); chi=getattr(self,"_chi_val",self._re)
        try:
            with open(CFG_PROGRESS,"w") as f:
                json.dump({"puzzle":self._pnum,"address":self._addr.get().strip(),
                           "start_hex":f"{clo:X}","end_hex":f"{chi:X}",
                           "start_pct":f"{val2frac(clo,self._rs,self._rt)*100:.6f}",
                           "end_pct":f"{val2frac(chi,self._rs,self._rt)*100:.6f}",
                           "mode":self._mode.get(),"started_at":datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
                          f,indent=2)
        except: pass

    # ── config ────────────────────────────────────────────────────────────────
    def _save_cfg(self):
        clo=getattr(self,"_clo_val",self._rs); chi=getattr(self,"_chi_val",self._re)
        try:
            with open(CFG_MAIN,"w") as f:
                json.dump({"exe":self._exe.get(),"puzzle_num":self._pnum,"gpu_id":self._gpu.get(),
                           "mode":self._mode.get(),"backup":self._bkp.get(),
                           "chunk_lo":f"{clo:X}","chunk_hi":f"{chi:X}",
                           "pct_lo":self._plo.get(),"pct_hi":self._phi.get()},f,indent=2)
            self._flash(self._cfgl,"✓ Saved")
        except Exception as ex: messagebox.showerror("Error",str(ex))

    def _apply_cfg(self,d):
        self._exe.set(d.get("exe","kk.exe")); self._gpu.set(d.get("gpu_id","0"))
        self._mode.set(d.get("mode","sequential")); self._bkp.set(d.get("backup",False))
        self._apply_puzzle(d.get("puzzle_num",71))
        lo=phex(d.get("chunk_lo","")); hi=phex(d.get("chunk_hi",""))
        if lo and hi and lo<hi: self._set_chunk(lo,hi)
        self._on_mode(); self._refresh()

    def _load_cfg(self,path=None):
        path=path or CFG_MAIN
        if not os.path.exists(path): self._apply_puzzle(71); return
        try:
            with open(path) as f: self._apply_cfg(json.load(f))
        except: self._apply_puzzle(71)

    def _load_cfg_dlg(self):
        path=filedialog.askopenfilename(title="Load config",filetypes=[("JSON","*.json"),("All","*.*")])
        if path:
            try:
                with open(path) as f: self._apply_cfg(json.load(f))
                self._flash(self._cfgl,"✓ Loaded")
            except Exception as ex: messagebox.showerror("Error",str(ex))

    # ── log ───────────────────────────────────────────────────────────────────
    def _log(self,text,tag="info"):
        self.log.config(state="normal"); ts=datetime.now().strftime("%H:%M:%S")
        self.log.insert("end",f"[{ts}] ","ts"); self.log.insert("end",text+"\n",tag)
        self.log.config(state="disabled"); self.log.see("end")

    def _clear_log(self): self.log.config(state="normal"); self.log.delete("1.0","end"); self.log.config(state="disabled")

    # ── misc ──────────────────────────────────────────────────────────────────
    def _flash(self,w,text): w.config(text=text,fg=GREEN); self.after(3000,lambda:w.config(text=""))
    def _browse_exe(self):
        p=filedialog.askopenfilename(title="Выбрать kk.exe",filetypes=[("Executable","*.exe"),("All","*.*")])
        if p: self._exe.set(p)
    def _open_folder(self):
        if sys.platform=="win32": os.startfile(os.path.dirname(os.path.abspath(__file__)))
    def _on_close(self): self._stop(); self._save_history(); self.destroy()

if __name__=="__main__":
    App().mainloop()
