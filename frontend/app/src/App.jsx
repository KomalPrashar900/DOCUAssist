import { useState, useRef, useEffect, useCallback } from "react";

/* ─── CSS ─────────────────────────────────────────────────────────────────── */
const CSS = `
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&family=JetBrains+Mono:wght@400;500&display=swap');

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}

:root{
  --bg0:#06070c;--bg1:#0d0f18;--bg2:#121520;--bg3:#181b29;--bg4:#1e2235;
  --bdr:rgba(255,255,255,0.055);--bdr2:rgba(255,255,255,0.10);
  --blue:#2563eb;--blue2:#3b82f6;--blue3:#60a5fa;
  --glow:rgba(37,99,235,0.20);--glow2:rgba(37,99,235,0.09);
  --text:#e8eaf0;--text2:#8b90a4;--text3:#4b5068;--text4:#2a2d3e;
  --green:#10b981;--gbg:rgba(16,185,129,0.09);
  --red:#ef4444;--rbg:rgba(239,68,68,0.09);
  --amber:#f59e0b;
  --font:'DM Sans',sans-serif;--mono:'JetBrains Mono',monospace;
  --r:10px;--r2:14px;--sidebar:268px;
}

body{font-family:var(--font);background:var(--bg0);color:var(--text);
  height:100vh;overflow:hidden;font-size:14px;line-height:1.65;
  -webkit-font-smoothing:antialiased;}

::-webkit-scrollbar{width:3px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--bdr2);border-radius:2px}

/* ── AUTH ── */
.auth-root{display:flex;height:100vh;align-items:center;justify-content:center;
  background:radial-gradient(ellipse 70% 55% at 50% -5%,rgba(37,99,235,0.13) 0%,transparent 68%),var(--bg0);}
.auth-card{background:var(--bg2);border:1px solid var(--bdr2);border-radius:20px;
  padding:36px 32px;width:370px;box-shadow:0 24px 64px rgba(0,0,0,0.5);}
.auth-brand{display:flex;align-items:center;gap:10px;justify-content:center;margin-bottom:24px;}
.auth-brand-icon{width:36px;height:36px;background:var(--blue);border-radius:9px;
  display:flex;align-items:center;justify-content:center;
  box-shadow:0 0 22px var(--glow);font-size:15px;}
.auth-brand-name{font-size:1.18rem;font-weight:700;letter-spacing:-0.4px;}
.auth-brand-name span{color:var(--blue3);}
.auth-sub{text-align:center;font-size:11.5px;color:var(--text3);margin-bottom:22px;}
.auth-tabs{display:flex;gap:3px;background:var(--bg3);border-radius:var(--r);
  padding:3px;margin-bottom:20px;}
.auth-tab{flex:1;padding:7px;text-align:center;border-radius:8px;cursor:pointer;
  font-size:12.5px;font-weight:500;color:var(--text2);transition:all .18s;}
.auth-tab.on{background:var(--bg4);color:var(--text);box-shadow:0 1px 4px rgba(0,0,0,.5);}
.auth-field{margin-bottom:13px;position:relative;}
.auth-field label{display:block;font-size:11.5px;font-weight:500;color:var(--text3);
  margin-bottom:5px;letter-spacing:.2px;}
.auth-field input{width:100%;background:var(--bg3);border:1px solid var(--bdr2);
  border-radius:9px;padding:9px 13px;color:var(--text);font-family:var(--font);
  font-size:13.5px;outline:none;transition:border-color .18s,box-shadow .18s;}
.auth-field input:focus{border-color:var(--blue);box-shadow:0 0 0 3px var(--glow2);}
.auth-field input.err{border-color:var(--red);}
.auth-field input::placeholder{color:var(--text4);}
.pw-wrap{position:relative;}
.pw-wrap input{padding-right:38px;}
.pw-eye{position:absolute;right:11px;top:50%;transform:translateY(-50%);
  background:none;border:none;color:var(--text3);cursor:pointer;padding:2px;
  display:flex;align-items:center;transition:color .15s;}
.pw-eye:hover{color:var(--text2);}
.auth-btn{width:100%;padding:10px;background:var(--blue);border:none;border-radius:9px;
  color:#fff;font-family:var(--font);font-size:13.5px;font-weight:600;cursor:pointer;
  transition:all .18s;margin-top:2px;box-shadow:0 0 0 rgba(37,99,235,0);}
.auth-btn:hover{background:var(--blue2);box-shadow:0 0 22px var(--glow);}
.auth-btn:disabled{opacity:.6;cursor:not-allowed;}
.auth-btn.secondary{background:transparent;border:1px solid var(--bdr2);color:var(--text2);
  box-shadow:none;margin-top:8px;}
.auth-btn.secondary:hover{border-color:var(--blue3);color:var(--blue3);box-shadow:none;}
.auth-err{background:var(--rbg);border:1px solid rgba(239,68,68,.2);border-radius:8px;
  padding:7px 11px;font-size:12px;color:var(--red);margin-bottom:11px;}
.auth-ok{background:var(--gbg);border:1px solid rgba(16,185,129,.2);border-radius:8px;
  padding:7px 11px;font-size:12px;color:var(--green);margin-bottom:11px;}
.auth-hint{text-align:center;font-size:11px;color:var(--text4);margin-top:14px;}
.auth-hint span{color:var(--blue3);cursor:pointer;}
.auth-hint span:hover{text-decoration:underline;}
.auth-remember{display:flex;align-items:center;gap:7px;margin-bottom:13px;cursor:pointer;}
.auth-remember input[type=checkbox]{width:14px;height:14px;accent-color:var(--blue);cursor:pointer;}
.auth-remember span{font-size:12px;color:var(--text3);}
.auth-forgot{display:block;text-align:right;font-size:11px;color:var(--blue3);
  cursor:pointer;margin-bottom:13px;margin-top:-8px;}
.auth-forgot:hover{text-decoration:underline;}

/* ── APP LAYOUT ── */
.app{display:flex;height:100vh;overflow:hidden;}

/* ── SIDEBAR ── */
.sidebar{width:var(--sidebar);background:var(--bg1);border-right:1px solid var(--bdr);
  display:flex;flex-direction:column;flex-shrink:0;overflow:hidden;
  transition:transform .25s ease;}
.sb-head{padding:14px 10px 10px;}
.sb-brand{display:flex;align-items:center;gap:8px;padding:0 4px;margin-bottom:12px;}
.sb-brand-icon{width:26px;height:26px;background:var(--blue);border-radius:7px;
  display:flex;align-items:center;justify-content:center;font-size:12px;
  box-shadow:0 0 12px var(--glow);flex-shrink:0;}
.sb-brand-name{font-size:.95rem;font-weight:700;letter-spacing:-.3px;}
.sb-brand-name span{color:var(--blue3);}
.new-btn{display:flex;align-items:center;gap:7px;width:100%;padding:8px 11px;
  background:transparent;border:1px solid var(--bdr2);border-radius:var(--r);
  color:var(--text2);font-family:var(--font);font-size:12.5px;font-weight:500;
  cursor:pointer;transition:all .18s;}
.new-btn:hover{border-color:var(--blue);color:var(--text);background:var(--glow2);}
.new-btn svg{opacity:.65;}

.hist-scroll{flex:1;overflow-y:auto;padding:4px 8px;}
.hist-label{font-size:9.5px;font-weight:600;letter-spacing:.8px;color:var(--text3);
  text-transform:uppercase;padding:8px 6px 4px;}
.hist-item{display:flex;align-items:center;gap:7px;padding:6px 8px;
  border-radius:8px;cursor:pointer;transition:background .14s;margin-bottom:1px;}
.hist-item:hover{background:var(--bg3);}
.hist-item.on{background:var(--bg4);}
.hist-dot{width:5px;height:5px;border-radius:50%;background:var(--blue);
  opacity:.45;flex-shrink:0;}
.hist-item.on .hist-dot{opacity:1;}
.hist-txt{font-size:12px;color:var(--text2);white-space:nowrap;overflow:hidden;
  text-overflow:ellipsis;flex:1;}
.hist-item.on .hist-txt{color:var(--text);}
.hist-del{width:18px;height:18px;border:none;background:transparent;color:var(--text3);
  cursor:pointer;border-radius:4px;display:none;align-items:center;justify-content:center;
  font-size:11px;flex-shrink:0;padding:0;}
.hist-item:hover .hist-del{display:flex;}
.hist-del:hover{color:var(--red);background:var(--rbg);}
.hist-empty{padding:10px 12px;font-size:12px;color:var(--text3);line-height:1.55;}

.sb-user{padding:11px 10px;border-top:1px solid var(--bdr);display:flex;
  align-items:center;gap:8px;}
.user-av{width:28px;height:28px;border-radius:50%;flex-shrink:0;
  background:linear-gradient(135deg,var(--blue),var(--blue3));
  display:flex;align-items:center;justify-content:center;
  font-size:11px;font-weight:700;color:#fff;}
.user-info{flex:1;min-width:0;}
.user-nm{font-size:12.5px;font-weight:600;color:var(--text);
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.user-em{font-size:10px;color:var(--text3);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.logout-btn{width:22px;height:22px;background:transparent;border:none;color:var(--text3);
  cursor:pointer;border-radius:5px;display:flex;align-items:center;justify-content:center;
  transition:all .15s;flex-shrink:0;}
.logout-btn:hover{color:var(--red);background:var(--rbg);}

/* ── MAIN ── */
.main{flex:1;display:flex;flex-direction:column;overflow:hidden;background:var(--bg0);min-width:0;}

.topbar{padding:13px 20px;border-bottom:1px solid var(--bdr);
  display:flex;align-items:center;justify-content:space-between;flex-shrink:0;gap:10px;}
.topbar-left{display:flex;align-items:center;gap:10px;min-width:0;}
.menu-btn{width:28px;height:28px;background:transparent;border:1px solid var(--bdr2);
  border-radius:7px;display:none;align-items:center;justify-content:center;
  color:var(--text2);cursor:pointer;flex-shrink:0;}
.menu-btn:hover{background:var(--bg3);}
.topbar-title{font-size:15px;font-weight:700;letter-spacing:-.3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.topbar-sub{font-size:11.5px;color:var(--text3);margin-top:2px;}
.upload-trigger{display:flex;align-items:center;gap:6px;padding:7px 14px;
  background:var(--blue);border:none;border-radius:var(--r);color:#fff;
  font-family:var(--font);font-size:12.5px;font-weight:600;cursor:pointer;
  transition:all .18s;box-shadow:0 0 16px var(--glow);white-space:nowrap;flex-shrink:0;}
.upload-trigger:hover{background:var(--blue2);box-shadow:0 0 24px var(--glow);transform:translateY(-1px);}

/* Upload panel */
.upload-panel{background:var(--bg2);border-bottom:1px solid var(--bdr);padding:14px 20px;
  animation:slideDown .22s ease;}
@keyframes slideDown{from{opacity:0;transform:translateY(-8px)}to{opacity:1;transform:none}}
.drop-zone{border:1.5px dashed var(--bdr2);border-radius:var(--r2);padding:18px;
  text-align:center;cursor:pointer;transition:all .18s;background:var(--bg3);}
.drop-zone:hover,.drop-zone.drag{border-color:var(--blue);background:var(--glow2);}
.drop-icon{font-size:20px;margin-bottom:5px;opacity:.55;}
.drop-txt{font-size:12.5px;color:var(--text2);line-height:1.5;}
.drop-txt span{color:var(--blue3);font-weight:500;}
.upload-row{display:flex;align-items:center;gap:9px;margin-top:9px;padding:8px 11px;
  background:var(--bg4);border-radius:8px;}
.spin{width:13px;height:13px;border:2px solid var(--bdr2);border-top-color:var(--blue);
  border-radius:50%;animation:spin .75s linear infinite;flex-shrink:0;}
@keyframes spin{to{transform:rotate(360deg)}}
.upload-fn{font-size:11.5px;color:var(--text2);flex:1;white-space:nowrap;
  overflow:hidden;text-overflow:ellipsis;}
.upload-ok{color:var(--green);font-size:11.5px;margin-top:6px;}

.doc-chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px;}
.doc-chip{display:flex;align-items:center;gap:6px;padding:5px 10px;
  background:var(--bg4);border:1px solid var(--bdr2);border-radius:20px;
  cursor:pointer;transition:all .15s;font-size:11.5px;user-select:none;}
.doc-chip.on{border-color:var(--blue);background:rgba(37,99,235,0.10);}
.doc-chip-dot{width:7px;height:7px;border-radius:50%;background:var(--bdr2);flex-shrink:0;}
.doc-chip.on .doc-chip-dot{background:var(--green);}
.doc-chip-name{color:var(--text2);max-width:160px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.doc-chip.on .doc-chip-name{color:var(--text);}
.doc-chip-pg{font-size:10px;color:var(--text3);}
.doc-chip-del{width:16px;height:16px;border:none;background:transparent;
  color:var(--text4);cursor:pointer;border-radius:50%;display:flex;align-items:center;
  justify-content:center;padding:0;flex-shrink:0;transition:all .14s;font-size:10px;line-height:1;}
.doc-chip-del:hover{color:var(--red);background:var(--rbg);}
.doc-actions{display:flex;gap:6px;margin-top:10px;}
.doc-action-btn{padding:4px 10px;border:1px solid var(--bdr2);border-radius:6px;
  background:transparent;color:var(--text3);font-size:11px;cursor:pointer;
  font-family:var(--font);transition:all .14s;}
.doc-action-btn:hover{border-color:var(--blue3);color:var(--blue3);}

/* Delete confirmation modal */
.modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,0.6);z-index:200;
  display:flex;align-items:center;justify-content:center;backdrop-filter:blur(3px);
  animation:fadeIn .18s ease;}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
.modal{background:var(--bg2);border:1px solid var(--bdr2);border-radius:16px;
  padding:28px 28px 22px;width:340px;box-shadow:0 24px 64px rgba(0,0,0,.6);
  animation:scaleIn .18s ease;}
@keyframes scaleIn{from{opacity:0;transform:scale(.95)}to{opacity:1;transform:none}}
.modal-title{font-size:15px;font-weight:600;margin-bottom:8px;}
.modal-body{font-size:13px;color:var(--text2);line-height:1.6;margin-bottom:20px;}
.modal-body strong{color:var(--text);}
.modal-actions{display:flex;gap:8px;justify-content:flex-end;}
.modal-btn{padding:8px 18px;border-radius:8px;font-family:var(--font);
  font-size:13px;font-weight:500;cursor:pointer;transition:all .15s;border:none;}
.modal-btn.cancel{background:var(--bg4);color:var(--text2);border:1px solid var(--bdr2);}
.modal-btn.cancel:hover{border-color:var(--bdr2);color:var(--text);}
.modal-btn.danger{background:var(--red);color:#fff;}
.modal-btn.danger:hover{background:#dc2626;}
.modal-btn:disabled{opacity:.55;cursor:not-allowed;}

/* Messages */
.msgs{flex:1;overflow-y:auto;padding:20px;}
.empty-state{display:flex;flex-direction:column;align-items:center;justify-content:center;
  height:100%;gap:14px;}
.empty-icon{width:52px;height:52px;background:var(--bg3);border:1px solid var(--bdr2);
  border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:22px;}
.empty-title{font-size:1rem;font-weight:600;}
.empty-sub{font-size:12.5px;color:var(--text3);text-align:center;max-width:340px;line-height:1.65;}
.chips{display:flex;flex-wrap:wrap;gap:7px;justify-content:center;margin-top:4px;}
.sug-chip{padding:7px 15px;border:1px solid var(--bdr2);border-radius:20px;
  font-size:12px;color:var(--text2);cursor:pointer;transition:all .18s;
  font-family:var(--font);}
.sug-chip:hover{border-color:var(--blue);color:var(--text);background:var(--glow2);}

.msg-row{display:flex;gap:11px;align-items:flex-start;margin-bottom:18px;
  animation:msgIn .22s ease;}
@keyframes msgIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.msg-row.usr{flex-direction:row-reverse;}
.m-av{width:28px;height:28px;border-radius:50%;flex-shrink:0;
  display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;}
.m-av.bot{background:var(--blue);box-shadow:0 0 12px var(--glow);}
.m-av.usr{background:var(--bg4);border:1px solid var(--bdr2);color:var(--text2);}
.m-body{flex:1;max-width:84%;}
.msg-row.usr .m-body{align-items:flex-end;display:flex;flex-direction:column;}
.bubble{padding:10px 14px;border-radius:13px;font-size:13.5px;line-height:1.7;}
.bubble.bot{background:var(--bg2);border:1px solid var(--bdr);
  border-radius:4px 13px 13px 13px;color:var(--text);}
.bubble.usr{background:var(--blue);border-radius:13px 4px 13px 13px;
  color:#fff;box-shadow:0 0 22px var(--glow);}
.bubble ul{padding-left:16px;margin-top:5px;}
.bubble li{margin-bottom:4px;color:var(--text2);}
.bubble.usr li{color:rgba(255,255,255,0.8);}
.bubble strong{color:var(--text);font-weight:600;}
.bubble.usr strong{color:#fff;}
.m-time{font-size:10px;color:var(--text3);margin-top:4px;font-family:var(--mono);}

.typing{display:flex;gap:4px;align-items:center;padding:3px 0;}
.td{width:6px;height:6px;background:var(--blue);border-radius:50%;
  animation:td 1.2s ease-in-out infinite;}
.td:nth-child(2){animation-delay:.2s}
.td:nth-child(3){animation-delay:.4s}
@keyframes td{0%,80%,100%{opacity:.3;transform:scale(.8)}40%{opacity:1;transform:scale(1)}}

/* Sources */
.src-toggle{display:flex;align-items:center;gap:5px;margin-top:7px;
  font-size:11.5px;color:var(--blue3);cursor:pointer;font-weight:500;
  padding:3px 0;width:fit-content;}
.src-toggle svg{transition:transform .18s;}
.src-toggle.open svg{transform:rotate(180deg);}
.src-list{margin-top:5px;display:flex;flex-direction:column;gap:4px;}
.src-card{display:flex;align-items:center;gap:9px;padding:7px 10px;
  background:var(--bg0);border:1px solid var(--bdr);border-radius:9px;
  cursor:pointer;transition:all .14s;}
.src-card:hover{border-color:var(--blue);background:var(--glow2);}
.src-file-ico{width:22px;height:22px;background:rgba(239,68,68,.10);border-radius:5px;
  display:flex;align-items:center;justify-content:center;font-size:10px;flex-shrink:0;}
.src-info{flex:1;min-width:0;}
.src-nm{font-size:11px;font-weight:500;color:var(--text);}
.src-pg{font-size:10px;color:var(--text3);font-family:var(--mono);margin-top:1px;}
.src-prev{font-size:10.5px;color:var(--text3);white-space:nowrap;overflow:hidden;
  text-overflow:ellipsis;max-width:200px;}

/* Actions */
.m-acts{display:flex;gap:4px;margin-top:5px;}
.act-btn{padding:3px 8px;border:1px solid var(--bdr);border-radius:5px;
  background:transparent;color:var(--text3);font-size:10px;cursor:pointer;
  transition:all .14s;font-family:var(--font);}
.act-btn:hover{border-color:var(--bdr2);color:var(--text2);background:var(--bg3);}
.act-btn.copied{color:var(--green);border-color:rgba(16,185,129,.3);}

/* Warn banner */
.warn-bar{display:flex;align-items:center;gap:7px;padding:8px 14px;
  background:rgba(245,158,11,0.07);border:1px solid rgba(245,158,11,0.18);
  border-radius:9px;margin-bottom:9px;font-size:12px;color:var(--amber);}

/* Input */
.input-bar{padding:13px 20px;border-top:1px solid var(--bdr);
  background:var(--bg0);flex-shrink:0;}
.input-wrap{display:flex;align-items:center;gap:9px;background:var(--bg2);
  border:1px solid var(--bdr2);border-radius:14px;padding:9px 13px;
  transition:border-color .18s,box-shadow .18s;}
.input-wrap:focus-within{border-color:var(--blue);box-shadow:0 0 0 3px var(--glow2);}
.input-wrap input{flex:1;background:transparent;border:none;outline:none;
  color:var(--text);font-family:var(--font);font-size:13.5px;}
.input-wrap input::placeholder{color:var(--text3);}
.send-btn{width:33px;height:33px;background:var(--blue);border:none;
  border-radius:9px;display:flex;align-items:center;justify-content:center;
  cursor:pointer;transition:all .15s;flex-shrink:0;box-shadow:0 0 14px var(--glow);}
.send-btn:hover{background:var(--blue2);transform:scale(1.05);}
.send-btn:disabled{opacity:.35;cursor:not-allowed;transform:none;}
.input-hint{font-size:10.5px;color:var(--text3);text-align:center;margin-top:7px;}
.kbd{display:inline;background:var(--bg3);border:1px solid var(--bdr2);
  border-radius:3px;padding:0 4px;font-family:var(--mono);font-size:9.5px;}

/* Mobile sidebar overlay */
.sidebar-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.6);
  z-index:99;backdrop-filter:blur(2px);}

/* ── RESPONSIVE ── */
@media(max-width:700px){
  :root{--sidebar:260px;}
  .sidebar{position:fixed;left:0;top:0;bottom:0;z-index:100;
    transform:translateX(-100%);}
  .sidebar.open{transform:translateX(0);}
  .sidebar-overlay.open{display:block;}
  .menu-btn{display:flex;}
  .topbar{padding:10px 14px;}
  .msgs{padding:12px;}
  .input-bar{padding:10px 12px;}
  .upload-panel{padding:10px 14px;}
  .topbar-sub{display:none;}
  .m-body{max-width:92%;}
}
@media(max-width:400px){
  .auth-card{width:94vw;padding:28px 18px;}
  .chips{flex-direction:column;align-items:center;}
}
`;

/* ─── Config ──────────────────────────────────────────────────────────────── */
const API = "http://localhost:8000/api";

/* ─── Helpers ─────────────────────────────────────────────────────────────── */
const uid  = () => Math.random().toString(36).slice(2, 10);
const now  = () => new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
const initials = (name = "") =>
  name.split(" ").map((w) => w[0]?.toUpperCase() || "").join("").slice(0, 2) || "U";

async function apiFetch(path, options = {}, token = null) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (token) headers["Authorization"] = `Bearer ${token}`;
  try {
    const res = await fetch(`http://localhost:8000${path}`, { ...options, headers });
    let data;
    try { data = await res.json(); } catch { data = {}; }
    return { ok: res.ok, status: res.status, data };
  } catch (err) {
    console.error("apiFetch error:", path, err);
    return { ok: false, status: 0, data: { detail: err.message } };
  }
}

/* ─── Eye icon ─────────────────────────────────────────────────────────────── */
function EyeIcon({ open }) {
  return open ? (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>
    </svg>
  ) : (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/>
    </svg>
  );
}

/* ─── Auth Screen ─────────────────────────────────────────────────────────── */
function AuthScreen({ onLogin, initialResetToken }) {
  // Determine initial view: if a reset token is in the URL, go straight to reset
  const [view, setView]         = useState(initialResetToken ? "reset" : "login");
  const [tab, setTab]           = useState("login");
  const [form, setForm]         = useState({ name: "", email: "", password: "", newPw: "", newPw2: "" });
  const [showPw, setShowPw]     = useState(false);
  const [showNewPw, setShowNewPw] = useState(false);
  const [remember, setRemember] = useState(false);
  const [err, setErr]           = useState("");
  const [ok, setOk]             = useState("");
  const [loading, setLoading]   = useState(false);
  const [resetToken]            = useState(initialResetToken || "");

  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }));

  async function submit() {
    setErr(""); setOk("");
    if (!form.email || !form.password) { setErr("Please fill in all fields."); return; }
    if (tab === "signup" && !form.name.trim()) { setErr("Name is required."); return; }
    if (tab === "signup" && form.password.length < 6) {
      setErr("Password must be at least 6 characters."); return;
    }
    setLoading(true);
    try {
      let res;
      if (tab === "login") {
        const body = new URLSearchParams({ username: form.email, password: form.password });
        res = await fetch(`${API}/auth/login`, {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body,
        });
      } else {
        res = await fetch(`${API}/auth/register`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name: form.name, email: form.email, password: form.password }),
        });
      }
      const data = await res.json();
      if (res.ok) {
        if (remember) {
          localStorage.setItem("da_remember_email", form.email);
        } else {
          localStorage.removeItem("da_remember_email");
        }
        onLogin(data.access_token, data.user);
      } else {
        setErr(data.detail || "Authentication failed.");
      }
    } catch {
      setErr("Cannot reach server. Make sure the backend is running.");
    } finally {  
      setLoading(false);
    }
  }

  async function submitForgot() {
    setErr(""); setOk("");
    if (!form.email) { setErr("Please enter your email address."); return; }
    setLoading(true);
    try {
      const res = await fetch(`${API}/auth/forgot-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: form.email }),
      });
      const data = await res.json();
      if (res.ok) {
        setOk(data.message);
      } else {
        setErr(data.detail || "Failed to send reset email.");
      }
    } catch {
      setErr("Cannot reach server.");
    } finally {
      setLoading(false);
    }
  }

  async function submitReset() {
    setErr(""); setOk("");
    if (!form.newPw || !form.newPw2) { setErr("Please fill in both fields."); return; }
    if (form.newPw.length < 6) { setErr("Password must be at least 6 characters."); return; }
    if (form.newPw !== form.newPw2) { setErr("Passwords do not match."); return; }
    setLoading(true);
    try {
      const res = await fetch(`${API}/auth/reset-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token: resetToken, new_password: form.newPw }),
      });
      const data = await res.json();
      if (res.ok) {
        setOk(data.message + " You can now sign in.");
        setTimeout(() => { setView("login"); setOk(""); }, 2500);
      } else {
        setErr(data.detail || "Reset failed.");
      }
    } catch {
      setErr("Cannot reach server.");
    } finally {
      setLoading(false);
    }
  }

  // Pre-fill remembered email
  useEffect(() => {
    const saved = localStorage.getItem("da_remember_email");
    if (saved) { setForm((f) => ({ ...f, email: saved })); setRemember(true); }
  }, []);

  const onKey = (fn) => (e) => { if (e.key === "Enter") fn(); };

  /* ── Forgot password view ── */
  if (view === "forgot") return (
    <div className="auth-root">
      <div className="auth-card">
        <div className="auth-brand">
          <div className="auth-brand-icon">📄</div>
          <div className="auth-brand-name">DOCU<span>Assist</span></div>
        </div>
        <div className="auth-sub">Enter your email to receive a reset link</div>
        {err && <div className="auth-err">{err}</div>}
        {ok  && <div className="auth-ok">{ok}</div>}
        {!ok && <>
          <div className="auth-field">
            <label>Email address</label>
            <input type="email" value={form.email} onChange={set("email")}
              placeholder="you@email.com" onKeyDown={onKey(submitForgot)} autoFocus/>
          </div>
          <button className="auth-btn" onClick={submitForgot} disabled={loading}>
            {loading ? "Sending…" : "Send reset link →"}
          </button>
        </>}
        <button className="auth-btn secondary" onClick={() => { setView("login"); setErr(""); setOk(""); }}>
          ← Back to sign in
        </button>
      </div>
    </div>
  );

  /* ── Reset password view ── */
  if (view === "reset") return (
    <div className="auth-root">
      <div className="auth-card">
        <div className="auth-brand">
          <div className="auth-brand-icon">📄</div>
          <div className="auth-brand-name">DOCU<span>Assist</span></div>
        </div>
        <div className="auth-sub">Create a new password</div>
        {err && <div className="auth-err">{err}</div>}
        {ok  && <div className="auth-ok">{ok}</div>}
        {!ok && <>
          <div className="auth-field">
            <label>New password</label>
            <div className="pw-wrap">
              <input type={showNewPw ? "text" : "password"} value={form.newPw}
                onChange={set("newPw")} placeholder="Min 6 characters" autoFocus/>
              <button className="pw-eye" onClick={() => setShowNewPw((v) => !v)} type="button">
                <EyeIcon open={showNewPw}/>
              </button>
            </div>
          </div>
          <div className="auth-field">
            <label>Confirm new password</label>
            <div className="pw-wrap">
              <input type={showNewPw ? "text" : "password"} value={form.newPw2}
                onChange={set("newPw2")} placeholder="Repeat password"
                onKeyDown={onKey(submitReset)}/>
              <button className="pw-eye" onClick={() => setShowNewPw((v) => !v)} type="button">
                <EyeIcon open={showNewPw}/>
              </button>
            </div>
          </div>
          <button className="auth-btn" onClick={submitReset} disabled={loading}>
            {loading ? "Saving…" : "Set new password →"}
          </button>
        </>}
        <button className="auth-btn secondary" onClick={() => { setView("login"); setErr(""); setOk(""); }}>
          ← Back to sign in
        </button>
      </div>
    </div>
  );

  /* ── Login / register view ── */
  return (
    <div className="auth-root">
      <div className="auth-card">
        <div className="auth-brand">
          <div className="auth-brand-icon">📄</div>
          <div className="auth-brand-name">DOCU<span>Assist</span></div>
        </div>
        <div className="auth-sub">AI-powered document intelligence</div>
        <div className="auth-tabs">
          {["login", "signup"].map((t) => (
            <div key={t} className={`auth-tab${tab === t ? " on" : ""}`}
              onClick={() => { setTab(t); setErr(""); setOk(""); }}>
              {t === "login" ? "Sign in" : "Create account"}
            </div>
          ))}
        </div>
        {err && <div className="auth-err">{err}</div>}
        {ok  && <div className="auth-ok">{ok}</div>}
        {tab === "signup" && (
          <div className="auth-field">
            <label>Name</label>
            <input value={form.name} onChange={set("name")} placeholder="Your name" autoFocus/>
          </div>
        )}
        <div className="auth-field">
          <label>Email</label>
          <input type="email" value={form.email} onChange={set("email")}
            placeholder="you@email.com" onKeyDown={onKey(submit)}
            autoFocus={tab === "login"}/>
        </div>
        <div className="auth-field">
          <label>Password</label>
          <div className="pw-wrap">
            <input type={showPw ? "text" : "password"} value={form.password}
              onChange={set("password")} placeholder="••••••••"
              onKeyDown={onKey(submit)}/>
            <button className="pw-eye" onClick={() => setShowPw((v) => !v)} type="button">
              <EyeIcon open={showPw}/>
            </button>
          </div>
        </div>
        {tab === "login" && (
          <>
            <label className="auth-remember">
              <input type="checkbox" checked={remember} onChange={(e) => setRemember(e.target.checked)}/>
              <span>Remember me</span>
            </label>
            <span className="auth-forgot" onClick={() => { setView("forgot"); setErr(""); setOk(""); }}>
              Forgot password?
            </span>
          </>
        )}
        <button className="auth-btn" onClick={submit} disabled={loading}>
          {loading ? "Please wait…" : tab === "login" ? "Sign in →" : "Create account →"}
        </button>
        <div className="auth-hint">
          {tab === "login" ? "Don't have an account? " : "Already have an account? "}
          <span onClick={() => { setTab(tab === "login" ? "signup" : "login"); setErr(""); setOk(""); }}>
            {tab === "login" ? "Create one" : "Sign in"}
          </span>
        </div>
      </div>
    </div>
  );
}

/* ─── Delete confirmation modal ────────────────────────────────────────────── */
function DeleteDocModal({ doc, onConfirm, onCancel, loading }) {
  return (
    <div className="modal-overlay" onClick={onCancel}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-title">Delete document?</div>
        <div className="modal-body">
          This will permanently delete <strong>{doc.name}</strong> and remove it from all future queries.
          This action cannot be undone.
        </div>
        <div className="modal-actions">
          <button className="modal-btn cancel" onClick={onCancel} disabled={loading}>Cancel</button>
          <button className="modal-btn danger" onClick={onConfirm} disabled={loading}>
            {loading ? "Deleting…" : "Delete"}
          </button>
        </div>
      </div>
    </div>
  );
}

/* ─── Message Component ───────────────────────────────────────────────────── */
function Message({ msg, userInitials }) {
  const isBot = msg.role === "assistant";
  const [srcOpen, setSrcOpen] = useState(false);
  const [copied, setCopied]   = useState(false);

  function copy() {
    navigator.clipboard?.writeText(msg.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 1600);
  }

  const lines = (msg.content || "").split("\n");

  return (
    <div className={`msg-row${isBot ? "" : " usr"}`}>
      <div className={`m-av${isBot ? " bot" : " usr"}`}>
        {isBot ? (
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 2a5 5 0 0 1 5 5v3H7V7a5 5 0 0 1 5-5z"/>
            <rect x="3" y="10" width="18" height="11" rx="3"/>
            <circle cx="9" cy="16" r="1" fill="white" stroke="none"/>
            <circle cx="15" cy="16" r="1" fill="white" stroke="none"/>
          </svg>
        ) : userInitials}
      </div>
      <div className="m-body">
        {msg.typing ? (
          <div className="bubble bot">
            <div className="typing">
              <div className="td"/><div className="td"/><div className="td"/>
            </div>
          </div>
        ) : (
          <>
            <div className={`bubble${isBot ? " bot" : " usr"}`}>
              {lines.map((line, i) => {
                if (!line) return <div key={i} style={{ height: 5 }} />;
                const html = line
                  .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
                  .replace(/`(.+?)`/g, `<code style="background:rgba(255,255,255,0.07);padding:1px 5px;border-radius:4px;font-family:var(--mono);font-size:12px;">$1</code>`);
                if (line.startsWith("• ") || line.startsWith("- ")) {
                  return (
                    <div key={i} style={{ display: "flex", gap: 7, alignItems: "flex-start", marginBottom: 3 }}>
                      <span style={{ color: "var(--blue3)", marginTop: 2, flexShrink: 0 }}>•</span>
                      <span dangerouslySetInnerHTML={{ __html: html.replace(/^[•\-]\s/, "") }}/>
                    </div>
                  );
                }
                return <div key={i} dangerouslySetInnerHTML={{ __html: html }}/>;
              })}
            </div>

            {isBot && msg.sources?.length > 0 && (
              <>
                <div className={`src-toggle${srcOpen ? " open" : ""}`} onClick={() => setSrcOpen((o) => !o)}>
                  <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"><path d="M6 9l6 6 6-6"/></svg>
                  Sources ({msg.sources.length})
                </div>
                {srcOpen && (
                  <div className="src-list">
                    {msg.sources.map((s, i) => (
                      <div className="src-card" key={i}>
                        <div className="src-file-ico">📕</div>
                        <div className="src-info">
                          <div className="src-nm">{s.filename}</div>
                          <div className="src-pg">Page {s.page}</div>
                        </div>
                        <div className="src-prev">{s.preview}</div>
                      </div>
                    ))}
                  </div>
                )}
              </>
            )}

            {isBot && (
              <div className="m-acts">
                <button className={`act-btn${copied ? " copied" : ""}`} onClick={copy}>
                  {copied ? "✓ Copied" : "Copy"}
                </button>
              </div>
            )}
            <div className="m-time">{msg.time}</div>
          </>
        )}
      </div>
    </div>
  );
}

/* ─── Main App ────────────────────────────────────────────────────────────── */
export default function DocuAssist() {
  // Check URL for a password-reset token (e.g. ?reset_token=xxx)
  const urlParams        = new URLSearchParams(window.location.search);
  const urlResetToken    = urlParams.get("reset_token") || "";

  const [token, setToken]               = useState(() => localStorage.getItem("da_token"));
  const [user, setUser]                 = useState(() => {
    try { return JSON.parse(localStorage.getItem("da_user") || "null"); } catch { return null; }
  });
  const [chats, setChats]               = useState([]);
  const [activeChatId, setActiveChatId] = useState(null);
  const [messages, setMessages]         = useState([]);
  const [docs, setDocs]                 = useState([]);
  const [activeDocIds, setActiveDocIds] = useState([]);
  const [showUpload, setShowUpload]     = useState(false);
  const [uploading, setUploading]       = useState(false);
  const [uploadFile, setUploadFile]     = useState("");
  const [uploadDone, setUploadDone]     = useState("");
  const [dragging, setDragging]         = useState(false);
  const [question, setQuestion]         = useState("");
  const [isAnswering, setIsAnswering]   = useState(false);
  const [sidebarOpen, setSidebarOpen]   = useState(false);
  const [loadingHistory, setLoadingHistory] = useState(false);
  // Document delete confirmation
  const [docToDelete, setDocToDelete]   = useState(null);
  const [deletingDoc, setDeletingDoc]   = useState(false);

  const fileRef = useRef(null);
  const msgsRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll on new message
  useEffect(() => {
    if (msgsRef.current) msgsRef.current.scrollTop = msgsRef.current.scrollHeight;
  }, [messages]);

  // Persist token/user across page refresh
  useEffect(() => {
    if (token) localStorage.setItem("da_token", token);
    else localStorage.removeItem("da_token");
  }, [token]);
  useEffect(() => {
    if (user) localStorage.setItem("da_user", JSON.stringify(user));
    else localStorage.removeItem("da_user");
  }, [user]);

  // Load initial data on mount if already logged in
  useEffect(() => {
    if (token) loadInitial(token);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Global keyboard shortcut: Ctrl/Cmd+K focuses input
  useEffect(() => {
    function onKey(e) {
      if ((e.ctrlKey || e.metaKey) && e.key === "k") {
        e.preventDefault();
        inputRef.current?.focus();
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  async function loadInitial(tok) {
    const [cr, dr] = await Promise.all([
      apiFetch("/api/chats", {}, tok),
      apiFetch("/api/documents", {}, tok),
    ]);
    if (cr.ok) setChats(cr.data);
    else if (cr.status === 401) { handleLogout(); return; }
    if (dr.ok) {
      setDocs(dr.data);
      setActiveDocIds(dr.data.map((d) => d.id));
    }
  }

  function handleLogin(tok, usr) {
    setToken(tok);
    setUser(usr);
    // Clean the URL if we came from a reset link
    if (urlResetToken) window.history.replaceState({}, "", window.location.pathname);
    loadInitial(tok);
  }

  function handleLogout() {
    setToken(null); setUser(null);
    setChats([]); setMessages([]);
    setDocs([]); setActiveDocIds([]);
    setActiveChatId(null);
    localStorage.removeItem("da_token");
    localStorage.removeItem("da_user");
  }

  async function newChat() {
    const { ok, data } = await apiFetch("/api/chats", {
      method: "POST", body: JSON.stringify({})
    }, token);
    if (ok) {
      setChats((prev) => [data, ...prev]);
      setActiveChatId(data.id);
      setMessages([]);
      setSidebarOpen(false);
    }
  }

  async function selectChat(id) {
    if (id === activeChatId) { setSidebarOpen(false); return; }
    setLoadingHistory(true);
    setActiveChatId(id);
    setMessages([]);
    const { ok, data } = await apiFetch(`/api/chats/${id}/messages`, {}, token);
    if (ok) setMessages(data.map((m) => ({ ...m, time: "" })));
    setLoadingHistory(false);
    setSidebarOpen(false);
  }

  async function deleteChat(id) {
    await apiFetch(`/api/chats/${id}`, { method: "DELETE" }, token);
    setChats((prev) => prev.filter((c) => c.id !== id));
    if (activeChatId === id) { setActiveChatId(null); setMessages([]); }
  }

  function toggleDoc(id) {
    setActiveDocIds((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );
  }

  function selectAllDocs() { setActiveDocIds(docs.map((d) => d.id)); }
  function selectNoDocs()   { setActiveDocIds([]); }

  // ── Document delete ─────────────────────────────────────────────────────────
  async function confirmDeleteDoc() {
    if (!docToDelete) return;
    setDeletingDoc(true);
    try {
      const { ok } = await apiFetch(`/api/documents/${docToDelete.id}`, { method: "DELETE" }, token);
      if (ok || true) { // remove from UI regardless (backend returns 'deleted' or 'not found')
        setDocs((prev) => prev.filter((d) => d.id !== docToDelete.id));
        setActiveDocIds((prev) => prev.filter((id) => id !== docToDelete.id));
      }
    } finally {
      setDeletingDoc(false);
      setDocToDelete(null);
    }
  }

  async function handleUpload(file) {
    if (!file || !file.name.toLowerCase().endsWith(".pdf")) {
      setUploadDone("Only PDF files allowed.");
      return;
    }
    setUploading(true);
    setUploadFile(file.name);
    setUploadDone("");
    try {
      const fd = new FormData();
      fd.append("file", file);
      const res = await fetch(`${API}/upload`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
        body: fd,
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Upload failed");
      const doc = {
        id: data.doc_id || data.id,
        name: data.name || data.filename,
        pages: data.pages,
        chunks: data.chunks,
      };
      setDocs((prev) => [doc, ...prev]);
      setActiveDocIds((prev) => [doc.id, ...prev]);
      setUploadDone(`✓ ${doc.name} — ${doc.pages} pages · ${doc.chunks} chunks indexed`);
    } catch (err) {
      setUploadDone(`Failed: ${err.message}`);
    } finally {
      setUploading(false);
    }
  }

  async function handleAsk() {
    if (!question.trim() || isAnswering || !activeDocIds.length) return;
    const q = question.trim();
    setQuestion("");
    setIsAnswering(true);

    const userMsg   = { id: uid(), role: "user",      content: q, time: now(), sources: [] };
    const typingMsg = { id: uid(), role: "assistant",  content: "", typing: true, time: now() };
    setMessages((p) => [...p, userMsg, typingMsg]);

    try {
      const res = await fetch(`${API}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
        body: JSON.stringify({ question: q, doc_ids: activeDocIds, chat_id: activeChatId ?? null }),
      });
      const data = await res.json();
      setMessages((prev) => {
        const without = prev.filter((m) => !m.typing);
        const botMsg = {
          id: uid(), role: "assistant",
          content: res.ok ? data.answer : `Error: ${data.detail || "Query failed"}`,
          sources: res.ok ? (data.sources || []) : [],
          time: now(),
        };
        return [...without, botMsg];
      });
      if (data.chat_id) {
        setActiveChatId(data.chat_id);
        setChats((prev) => {
          const exists = prev.find((c) => c.id === data.chat_id);
          if (exists) {
            return prev.map((c) =>
              c.id === data.chat_id
                ? { ...c, title: c.title === "New conversation" ? q.slice(0, 55) : c.title }
                : c
            );
          }
          return [{ id: data.chat_id, title: q.slice(0, 55) }, ...prev];
        });
      }
    } catch {
      setMessages((prev) => [
        ...prev.filter((m) => !m.typing),
        { id: uid(), role: "assistant", content: "Server error — is the backend running?", sources: [], time: now() },
      ]);
    } finally {
      setIsAnswering(false);
    }
  }

  const SUGGESTIONS = [
    "What is the main topic of this document?",
    "Summarize the key points",
    "List all important dates mentioned",
    "What are the conclusions or recommendations?",
  ];

  if (!token || urlResetToken) {
    return (
      <>
        <style>{CSS}</style>
        <AuthScreen onLogin={handleLogin} initialResetToken={urlResetToken}/>
      </>
    );
  }

  const userInits = initials(user?.name || "U");

  return (
    <>
      <style>{CSS}</style>
      {/* Delete confirmation modal */}
      {docToDelete && (
        <DeleteDocModal
          doc={docToDelete}
          onConfirm={confirmDeleteDoc}
          onCancel={() => setDocToDelete(null)}
          loading={deletingDoc}
        />
      )}

      <div className="app">
        <div className={`sidebar-overlay${sidebarOpen ? " open" : ""}`}
          onClick={() => setSidebarOpen(false)} />

        {/* ── SIDEBAR ── */}
        <div className={`sidebar${sidebarOpen ? " open" : ""}`}>
          <div className="sb-head">
            <div className="sb-brand">
              <div className="sb-brand-icon">📄</div>
              <div className="sb-brand-name">DOCU<span>Assist</span></div>
            </div>
            <button className="new-btn" onClick={newChat}>
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
              New conversation
            </button>
          </div>

          <div className="hist-scroll">
            {chats.length === 0
              ? <div className="hist-empty">No conversations yet.<br/>Upload a PDF and start asking.</div>
              : <>
                  <div className="hist-label">Conversations</div>
                  {chats.map((c) => (
                    <div key={c.id} className={`hist-item${c.id === activeChatId ? " on" : ""}`}
                      onClick={() => selectChat(c.id)}>
                      <div className="hist-dot"/>
                      <div className="hist-txt">{c.title || "New conversation"}</div>
                      <button className="hist-del"
                        onClick={(e) => { e.stopPropagation(); deleteChat(c.id); }}>
                        <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                      </button>
                    </div>
                  ))}
                </>
            }
          </div>

          <div className="sb-user">
            <div className="user-av">{userInits}</div>
            <div className="user-info">
              <div className="user-nm">{user?.name || "User"}</div>
              <div className="user-em">{user?.email}</div>
            </div>
            <button className="logout-btn" onClick={handleLogout} title="Sign out">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                <polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>
              </svg>
            </button>
          </div>
        </div>

        {/* ── MAIN ── */}
        <div className="main">
          {/* Topbar */}
          <div className="topbar">
            <div className="topbar-left">
              <button className="menu-btn" onClick={() => setSidebarOpen((o) => !o)}>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
              </button>
              <div>
                <div className="topbar-title">Document Intelligent Assistant</div>
                <div className="topbar-sub">Answers sourced exclusively from your uploaded PDFs</div>
              </div>
            </div>
            <button className="upload-trigger"
              onClick={() => { setShowUpload((o) => !o); setUploadDone(""); }}>
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/>
              </svg>
              Upload PDF{docs.length > 0 && ` · ${docs.length}`}
            </button>
          </div>

          {/* Upload panel */}
          {showUpload && (
            <div className="upload-panel">
              <div
                className={`drop-zone${dragging ? " drag" : ""}`}
                onClick={() => fileRef.current?.click()}
                onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
                onDragLeave={() => setDragging(false)}
                onDrop={(e) => { e.preventDefault(); setDragging(false); handleUpload(e.dataTransfer.files[0]); }}
              >
                <div className="drop-icon">☁</div>
                <div className="drop-txt">Drag & drop your PDF here<br/>or <span>click to browse</span></div>
                <input ref={fileRef} type="file" accept=".pdf" style={{ display: "none" }}
                  onChange={(e) => { handleUpload(e.target.files[0]); e.target.value = ""; }}/>
              </div>

              {uploading && (
                <div className="upload-row">
                  <div className="spin"/>
                  <span className="upload-fn">Processing {uploadFile}…</span>
                </div>
              )}
              {uploadDone && <div className="upload-ok">{uploadDone}</div>}

              {docs.length > 0 && (
                <div style={{ marginTop: 12 }}>
                  <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 6 }}>
                    <div style={{ fontSize: 11, color: "var(--text3)", fontWeight: 500 }}>
                      Select documents for search ({activeDocIds.length}/{docs.length} active):
                    </div>
                    <div className="doc-actions">
                      <button className="doc-action-btn" onClick={selectAllDocs}>All</button>
                      <button className="doc-action-btn" onClick={selectNoDocs}>None</button>
                    </div>
                  </div>
                  <div className="doc-chips">
                    {docs.map((d) => {
                      const on = activeDocIds.includes(d.id);
                      return (
                        <div key={d.id} className={`doc-chip${on ? " on" : ""}`}
                          onClick={() => toggleDoc(d.id)}>
                          <div className="doc-chip-dot"/>
                          <span className="doc-chip-name">{d.name}</span>
                          <span className="doc-chip-pg">{d.pages}p</span>
                          {/* Delete button — stops propagation so it doesn't also toggle */}
                          <button
                            className="doc-chip-del"
                            title="Delete document"
                            onClick={(e) => { e.stopPropagation(); setDocToDelete(d); }}
                          >
                            <svg width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
                              <polyline points="3 6 5 6 21 6"/>
                              <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>
                              <path d="M10 11v6"/><path d="M14 11v6"/>
                              <path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/>
                            </svg>
                          </button>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Messages */}
          <div className="msgs" ref={msgsRef}>
            {loadingHistory ? (
              <div className="empty-state">
                <div className="spin" style={{ width: 22, height: 22, borderWidth: 3 }}/>
              </div>
            ) : messages.length === 0 ? (
              <div className="empty-state">
                <div className="empty-icon">📄</div>
                <div className="empty-title">Welcome, {user?.name?.split(" ")[0] || "there"}</div>
                <div className="empty-sub">
                  {docs.length === 0
                    ? "Upload a PDF using the button above, then ask anything about its content."
                    : `${docs.length} document${docs.length > 1 ? "s" : ""} ready. Ask anything about your PDFs.`}
                </div>
                <div className="chips">
                  {SUGGESTIONS.map((s) => (
                    <button key={s} className="sug-chip"
                      onClick={() => { if (!activeDocIds.length) return; setQuestion(s); inputRef.current?.focus(); }}>
                      "{s}"
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              messages.map((msg) => (
                <Message key={msg.id} msg={msg} userInitials={userInits}/>
              ))
            )}
          </div>

          {/* Input */}
          <div className="input-bar">
            {activeDocIds.length === 0 && docs.length > 0 && (
              <div className="warn-bar">
                <span>⚠</span> No documents selected — click "Upload PDF" to select documents.
              </div>
            )}
            <div className="input-wrap">
              <input
                ref={inputRef}
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && handleAsk()}
                placeholder={
                  activeDocIds.length
                    ? "Ask a question about your documents…"
                    : "Upload a PDF first, then ask questions…"
                }
                disabled={isAnswering}
              />
              <button className="send-btn" onClick={handleAsk}
                disabled={!question.trim() || isAnswering || !activeDocIds.length}>
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none">
                  <path d="M22 2L11 13" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  <path d="M22 2L15 22 11 13 2 9l20-7z" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </button>
            </div>
            <div className="input-hint">
              Press <span className="kbd">Enter</span> to send · <span className="kbd">Ctrl K</span> to focus · RAG + FAISS · FastAPI + Gemini
            </div>
          </div>
        </div>
      </div>
    </>
  );
}






