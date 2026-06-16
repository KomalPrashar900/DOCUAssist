import { useState, useRef, useEffect } from "react";

const CSS = `
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500&display=swap');

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}

:root{
  --ink0:#0a0b10;--ink1:#0f111a;--ink2:#151822;--ink3:#1c2030;--ink4:#232840;
  --rail:rgba(255,255,255,0.05);--rail2:rgba(255,255,255,0.09);--rail3:rgba(255,255,255,0.14);
  --iris:#5b6af0;--iris2:#7482f7;--iris3:#9ba7ff;--iris4:rgba(91,106,240,0.12);--iris5:rgba(91,106,240,0.06);
  --jade:#22c9a0;--jbg:rgba(34,201,160,0.08);
  --rose:#f04a6b;--rbg:rgba(240,74,107,0.08);
  --sun:#f5a623;--sbg:rgba(245,166,35,0.09);
  --ink:#dde2f0;--ink-2:#8891b4;--ink-3:#4a5070;--ink-4:#272d47;
  --font:'Inter',sans-serif;--serif:'Instrument Serif',Georgia,serif;--mono:'JetBrains Mono',monospace;
  --r:10px;--r2:14px;--r3:18px;--sidebar:272px;
}

body{font-family:var(--font);background:var(--ink0);color:var(--ink);height:100vh;overflow:hidden;
  font-size:14px;line-height:1.6;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;}

::-webkit-scrollbar{width:3px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--rail2);border-radius:4px}
::-webkit-scrollbar-thumb:hover{background:var(--rail3)}

/* ═══ AUTH ═══════════════════════════════════════════════════════════════════ */

.auth-root{display:flex;height:100vh;overflow:hidden;}

/* left panel — decorative */
.auth-left{width:420px;flex-shrink:0;background:var(--ink1);border-right:1px solid var(--rail);
  display:flex;flex-direction:column;justify-content:space-between;padding:40px;
  position:relative;overflow:hidden;}
.auth-left-glow{position:absolute;width:480px;height:480px;border-radius:50%;
  background:radial-gradient(circle,rgba(91,106,240,0.18) 0%,transparent 65%);
  top:-140px;left:-120px;pointer-events:none;}
.auth-left-glow2{position:absolute;width:320px;height:320px;border-radius:50%;
  background:radial-gradient(circle,rgba(34,201,160,0.10) 0%,transparent 70%);
  bottom:-80px;right:-80px;pointer-events:none;}
.auth-wordmark{display:flex;align-items:center;gap:11px;position:relative;}
.auth-logo{width:34px;height:34px;background:var(--iris);border-radius:9px;
  display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.auth-logo svg{display:block;}
.auth-wordmark-text{font-size:1.05rem;font-weight:700;letter-spacing:-0.3px;color:var(--ink);}
.auth-wordmark-text em{font-style:normal;color:var(--iris3);}
.auth-hero{position:relative;flex:1;display:flex;flex-direction:column;justify-content:center;gap:20px;}
.auth-tagline{font-family:var(--serif);font-size:2.2rem;font-weight:400;line-height:1.25;
  color:var(--ink);letter-spacing:-0.5px;}
.auth-tagline em{font-style:italic;color:var(--iris3);}
.auth-desc{font-size:13px;color:var(--ink-2);line-height:1.7;max-width:300px;}
.auth-pills{display:flex;flex-wrap:wrap;gap:7px;margin-top:4px;}
.auth-pill{padding:5px 12px;background:var(--ink2);border:1px solid var(--rail2);
  border-radius:20px;font-size:11.5px;color:var(--ink-2);}
.auth-footer-txt{font-size:11px;color:var(--ink-3);position:relative;}

/* right panel — form */
.auth-right{flex:1;display:flex;align-items:center;justify-content:center;
  background:var(--ink0);padding:40px;overflow-y:auto;}
.auth-form-box{width:100%;max-width:380px;}
.auth-form-title{font-size:1.35rem;font-weight:700;letter-spacing:-0.4px;margin-bottom:4px;}
.auth-form-sub{font-size:12.5px;color:var(--ink-2);margin-bottom:28px;}
.auth-tabs{display:flex;gap:2px;background:var(--ink2);border-radius:var(--r);
  padding:3px;margin-bottom:24px;border:1px solid var(--rail);}
.auth-tab{flex:1;padding:7px;text-align:center;border-radius:8px;cursor:pointer;
  font-size:12.5px;font-weight:500;color:var(--ink-2);transition:all .2s;user-select:none;}
.auth-tab.on{background:var(--iris4);color:var(--iris3);
  box-shadow:inset 0 0 0 1px rgba(91,106,240,0.25);}
.auth-field{margin-bottom:14px;}
.auth-field label{display:block;font-size:11.5px;font-weight:500;color:var(--ink-3);
  margin-bottom:6px;letter-spacing:.15px;text-transform:uppercase;}
.auth-field input{width:100%;background:var(--ink2);border:1px solid var(--rail2);
  border-radius:var(--r);padding:10px 14px;color:var(--ink);font-family:var(--font);
  font-size:13.5px;outline:none;transition:border-color .18s,box-shadow .18s;}
.auth-field input:focus{border-color:var(--iris);box-shadow:0 0 0 3px var(--iris4);}
.auth-field input::placeholder{color:var(--ink-4);}
.pw-wrap{position:relative;}
.pw-wrap input{padding-right:40px;}
.pw-eye{position:absolute;right:12px;top:50%;transform:translateY(-50%);
  background:none;border:none;color:var(--ink-3);cursor:pointer;padding:2px;
  display:flex;align-items:center;transition:color .15s;}
.pw-eye:hover{color:var(--ink-2);}
.auth-meta{display:flex;align-items:center;justify-content:space-between;margin-bottom:18px;}
.auth-remember{display:flex;align-items:center;gap:6px;cursor:pointer;user-select:none;}
.auth-remember input{width:14px;height:14px;accent-color:var(--iris);cursor:pointer;border-radius:3px;}
.auth-remember span{font-size:12px;color:var(--ink-2);}
.auth-forgot{font-size:12px;color:var(--iris2);cursor:pointer;background:none;border:none;
  font-family:var(--font);padding:0;transition:color .15s;}
.auth-forgot:hover{color:var(--iris3);}
.auth-submit{width:100%;padding:11px;background:var(--iris);border:none;border-radius:var(--r);
  color:#fff;font-family:var(--font);font-size:13.5px;font-weight:600;cursor:pointer;
  transition:all .2s;position:relative;overflow:hidden;letter-spacing:.1px;}
.auth-submit::after{content:'';position:absolute;inset:0;
  background:linear-gradient(180deg,rgba(255,255,255,0.06) 0%,transparent 100%);pointer-events:none;}
.auth-submit:hover{background:var(--iris2);transform:translateY(-1px);}
.auth-submit:active{transform:translateY(0);}
.auth-submit:disabled{opacity:.55;cursor:not-allowed;transform:none;}
.auth-submit.secondary{background:var(--ink2);color:var(--ink-2);border:1px solid var(--rail2);
  margin-top:10px;}
.auth-submit.secondary::after{display:none;}
.auth-submit.secondary:hover{border-color:var(--rail3);color:var(--ink);background:var(--ink3);}
.auth-divider{text-align:center;font-size:11px;color:var(--ink-3);margin:16px 0;}
.auth-hint{text-align:center;font-size:12px;color:var(--ink-3);margin-top:18px;}
.auth-hint b{color:var(--iris2);cursor:pointer;font-weight:500;}
.auth-hint b:hover{color:var(--iris3);text-decoration:underline;}
.auth-err{display:flex;align-items:center;gap:8px;background:var(--rbg);
  border:1px solid rgba(240,74,107,.2);border-radius:var(--r);
  padding:9px 12px;font-size:12.5px;color:var(--rose);margin-bottom:14px;}
.auth-ok{display:flex;align-items:center;gap:8px;background:var(--jbg);
  border:1px solid rgba(34,201,160,.2);border-radius:var(--r);
  padding:9px 12px;font-size:12.5px;color:var(--jade);margin-bottom:14px;}

/* ═══ APP CHROME ═════════════════════════════════════════════════════════════ */

.app{display:flex;height:100vh;overflow:hidden;}

/* ── SIDEBAR ── */
.sidebar{width:var(--sidebar);background:var(--ink1);border-right:1px solid var(--rail);
  display:flex;flex-direction:column;flex-shrink:0;overflow:hidden;transition:transform .28s cubic-bezier(.4,0,.2,1);}

.sb-top{padding:16px 12px 12px;}
.sb-logo{display:flex;align-items:center;gap:9px;padding:0 4px 14px;}
.sb-logo-icon{width:24px;height:24px;background:var(--iris);border-radius:6px;
  display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.sb-logo-name{font-size:.9rem;font-weight:700;letter-spacing:-.2px;}
.sb-logo-name em{font-style:normal;color:var(--iris3);}

.new-chat-btn{display:flex;align-items:center;gap:8px;width:100%;padding:9px 12px;
  background:var(--iris4);border:1px solid rgba(91,106,240,0.22);border-radius:var(--r);
  color:var(--iris3);font-family:var(--font);font-size:12.5px;font-weight:600;
  cursor:pointer;transition:all .18s;letter-spacing:.1px;}
.new-chat-btn:hover{background:rgba(91,106,240,0.18);border-color:rgba(91,106,240,0.35);}
.new-chat-btn svg{flex-shrink:0;opacity:.8;}

.hist-body{flex:1;overflow-y:auto;padding:6px 8px;}
.hist-group-lbl{font-size:9.5px;font-weight:600;letter-spacing:1px;color:var(--ink-3);
  text-transform:uppercase;padding:10px 8px 4px;}
.hist-row{display:flex;align-items:center;gap:7px;padding:7px 9px;
  border-radius:9px;cursor:pointer;transition:background .14s;margin-bottom:1px;group:true;}
.hist-row:hover{background:var(--ink2);}
.hist-row.active{background:var(--ink3);}
.hist-row-icon{width:16px;height:16px;opacity:.3;flex-shrink:0;transition:opacity .14s;}
.hist-row:hover .hist-row-icon,.hist-row.active .hist-row-icon{opacity:.55;}
.hist-row-txt{font-size:12px;color:var(--ink-2);white-space:nowrap;overflow:hidden;
  text-overflow:ellipsis;flex:1;transition:color .14s;}
.hist-row.active .hist-row-txt{color:var(--ink);}
.hist-del-btn{width:18px;height:18px;border:none;background:transparent;color:var(--ink-3);
  cursor:pointer;border-radius:4px;display:none;align-items:center;justify-content:center;flex-shrink:0;}
.hist-row:hover .hist-del-btn{display:flex;}
.hist-del-btn:hover{color:var(--rose);background:var(--rbg);}
.hist-none{padding:12px 16px;font-size:12px;color:var(--ink-3);line-height:1.6;}

.sb-bottom{padding:10px 12px;border-top:1px solid var(--rail);}
.user-row{display:flex;align-items:center;gap:9px;}
.user-av{width:30px;height:30px;border-radius:50%;flex-shrink:0;
  background:linear-gradient(135deg,var(--iris),var(--iris3));
  display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#fff;}
.user-details{flex:1;min-width:0;}
.user-name{font-size:12.5px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.user-email{font-size:10.5px;color:var(--ink-3);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.signout-btn{width:24px;height:24px;background:transparent;border:none;color:var(--ink-3);
  cursor:pointer;border-radius:6px;display:flex;align-items:center;justify-content:center;transition:all .15s;}
.signout-btn:hover{color:var(--rose);background:var(--rbg);}

/* ── MAIN PANEL ── */
.main{flex:1;display:flex;flex-direction:column;overflow:hidden;background:var(--ink0);min-width:0;}

/* topbar */
.topbar{display:flex;align-items:center;justify-content:space-between;
  padding:12px 22px;border-bottom:1px solid var(--rail);flex-shrink:0;gap:12px;}
.topbar-left{display:flex;align-items:center;gap:10px;min-width:0;}
.ham-btn{width:28px;height:28px;background:transparent;border:1px solid var(--rail2);
  border-radius:7px;display:none;align-items:center;justify-content:center;
  color:var(--ink-2);cursor:pointer;flex-shrink:0;}
.ham-btn:hover{background:var(--ink2);}
.chat-title{font-size:14.5px;font-weight:700;letter-spacing:-.3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.chat-sub{font-size:11px;color:var(--ink-3);margin-top:1px;}
.upload-btn{display:flex;align-items:center;gap:7px;padding:8px 16px;
  background:var(--iris);border:none;border-radius:var(--r);color:#fff;
  font-family:var(--font);font-size:12.5px;font-weight:600;cursor:pointer;
  transition:all .2s;white-space:nowrap;flex-shrink:0;letter-spacing:.1px;}
.upload-btn:hover{background:var(--iris2);transform:translateY(-1px);}
.upload-btn:active{transform:none;}
.doc-count-badge{background:rgba(255,255,255,0.15);border-radius:20px;
  padding:1px 7px;font-size:11px;font-weight:600;}

/* upload drawer */
.upload-drawer{background:var(--ink1);border-bottom:1px solid var(--rail);
  padding:16px 22px;animation:drawDown .2s ease;}
@keyframes drawDown{from{opacity:0;transform:translateY(-10px)}to{opacity:1;transform:none}}
.dropzone{border:1.5px dashed var(--rail2);border-radius:var(--r2);padding:20px;
  text-align:center;cursor:pointer;transition:all .2s;background:var(--ink0);}
.dropzone:hover,.dropzone.over{border-color:var(--iris);background:var(--iris5);}
.dz-icon{font-size:22px;margin-bottom:6px;opacity:.5;}
.dz-txt{font-size:12.5px;color:var(--ink-2);line-height:1.55;}
.dz-txt b{color:var(--iris3);font-weight:500;}
.upload-progress{display:flex;align-items:center;gap:10px;margin-top:10px;
  padding:9px 12px;background:var(--ink2);border-radius:var(--r);}
.spinner{width:14px;height:14px;border:2px solid var(--rail2);border-top-color:var(--iris);
  border-radius:50%;animation:spin .7s linear infinite;flex-shrink:0;}
@keyframes spin{to{transform:rotate(360deg)}}
.upload-fname{font-size:12px;color:var(--ink-2);flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.upload-result{margin-top:8px;font-size:12px;}
.upload-result.ok{color:var(--jade);}
.upload-result.err{color:var(--rose);}

/* doc library */
.doc-lib{margin-top:14px;}
.doc-lib-hdr{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;}
.doc-lib-label{font-size:10.5px;font-weight:600;letter-spacing:.7px;text-transform:uppercase;color:var(--ink-3);}
.doc-ctrl-row{display:flex;gap:5px;}
.doc-ctrl-btn{padding:3px 9px;border:1px solid var(--rail2);border-radius:5px;
  background:transparent;color:var(--ink-3);font-size:11px;cursor:pointer;font-family:var(--font);transition:all .14s;}
.doc-ctrl-btn:hover{border-color:var(--iris);color:var(--iris3);}
.doc-chips{display:flex;flex-wrap:wrap;gap:6px;}
.doc-chip{display:flex;align-items:center;gap:6px;padding:5px 10px;
  background:var(--ink3);border:1px solid var(--rail2);border-radius:20px;
  cursor:pointer;transition:all .15s;font-size:11.5px;user-select:none;}
.doc-chip.active{border-color:var(--iris);background:var(--iris4);}
.doc-chip-dot{width:6px;height:6px;border-radius:50%;background:var(--ink-3);flex-shrink:0;transition:background .15s;}
.doc-chip.active .doc-chip-dot{background:var(--jade);}
.doc-chip-name{color:var(--ink-2);max-width:160px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.doc-chip.active .doc-chip-name{color:var(--ink);}
.doc-chip-pg{font-size:10px;color:var(--ink-3);}
.doc-chip-del{width:15px;height:15px;border:none;background:transparent;color:var(--ink-4);
  cursor:pointer;border-radius:50%;display:flex;align-items:center;justify-content:center;
  padding:0;flex-shrink:0;transition:all .14s;}
.doc-chip-del:hover{color:var(--rose);background:var(--rbg);}

/* confirm modal */
.modal-veil{position:fixed;inset:0;background:rgba(0,0,0,0.55);z-index:300;
  display:flex;align-items:center;justify-content:center;backdrop-filter:blur(4px);
  animation:fadeIn .15s ease;}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
.modal-box{background:var(--ink2);border:1px solid var(--rail2);border-radius:var(--r3);
  padding:28px;width:330px;box-shadow:0 32px 80px rgba(0,0,0,.7);
  animation:popIn .18s ease;}
@keyframes popIn{from{opacity:0;transform:scale(.94)}to{opacity:1;transform:none}}
.modal-title{font-size:15px;font-weight:700;margin-bottom:8px;}
.modal-body{font-size:12.5px;color:var(--ink-2);line-height:1.65;margin-bottom:22px;}
.modal-body strong{color:var(--ink);}
.modal-btns{display:flex;gap:8px;justify-content:flex-end;}
.modal-cancel{padding:8px 18px;border-radius:8px;font-family:var(--font);font-size:13px;
  font-weight:500;cursor:pointer;transition:all .15s;background:var(--ink3);
  color:var(--ink-2);border:1px solid var(--rail2);}
.modal-cancel:hover{color:var(--ink);border-color:var(--rail3);}
.modal-delete{padding:8px 18px;border-radius:8px;font-family:var(--font);font-size:13px;
  font-weight:600;cursor:pointer;transition:all .15s;background:var(--rose);color:#fff;border:none;}
.modal-delete:hover{filter:brightness(1.1);}
.modal-delete:disabled{opacity:.55;cursor:not-allowed;}

/* ═══ MESSAGES ══════════════════════════════════════════════════════════════ */

.msgs-area{flex:1;overflow-y:auto;padding:28px 24px;}

/* welcome state */
.welcome{display:flex;flex-direction:column;align-items:center;justify-content:center;
  height:100%;gap:16px;text-align:center;}
.welcome-orb{width:58px;height:58px;background:var(--iris4);border:1px solid rgba(91,106,240,0.25);
  border-radius:18px;display:flex;align-items:center;justify-content:center;}
.welcome-title{font-size:1.15rem;font-weight:700;letter-spacing:-.3px;}
.welcome-sub{font-size:13px;color:var(--ink-2);max-width:360px;line-height:1.7;}
.sug-row{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-top:6px;}
.sug-btn{padding:8px 16px;border:1px solid var(--rail2);border-radius:20px;
  font-size:12px;color:var(--ink-2);cursor:pointer;transition:all .2s;
  font-family:var(--font);background:transparent;}
.sug-btn:hover{border-color:var(--iris);color:var(--iris3);background:var(--iris5);}

/* message bubbles */
.msg{display:flex;gap:12px;align-items:flex-start;margin-bottom:22px;
  animation:msgUp .2s ease;}
@keyframes msgUp{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.msg.user{flex-direction:row-reverse;}
.msg-avatar{width:30px;height:30px;border-radius:50%;flex-shrink:0;
  display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;}
.msg-avatar.bot{background:var(--iris);box-shadow:0 0 0 3px var(--iris4);}
.msg-avatar.usr{background:var(--ink3);border:1px solid var(--rail2);color:var(--ink-2);}
.msg-body{flex:1;max-width:82%;min-width:0;}
.msg.user .msg-body{display:flex;flex-direction:column;align-items:flex-end;}

.bubble{padding:11px 15px;border-radius:16px;font-size:13.5px;line-height:1.72;}
.bubble.bot{background:var(--ink2);border:1px solid var(--rail);
  border-radius:4px 16px 16px 16px;color:var(--ink);}
.bubble.user{background:var(--iris);border-radius:16px 4px 16px 16px;
  color:#fff;box-shadow:0 4px 20px rgba(91,106,240,0.3);}
.bubble strong{font-weight:600;}
.bubble.bot strong{color:var(--ink);}
.bubble.user strong{color:#fff;}
.bubble code{background:rgba(255,255,255,0.08);padding:1px 6px;border-radius:4px;
  font-family:var(--mono);font-size:12px;}

/* typing dots */
.typing-dots{display:flex;gap:4px;align-items:center;padding:4px 0;}
.dot{width:6px;height:6px;background:var(--iris2);border-radius:50%;
  animation:pulse 1.4s ease-in-out infinite;}
.dot:nth-child(2){animation-delay:.2s}
.dot:nth-child(3){animation-delay:.4s}
@keyframes pulse{0%,80%,100%{opacity:.3;transform:scale(.85)}40%{opacity:1;transform:scale(1)}}

/* sources */
.src-toggle{display:flex;align-items:center;gap:5px;margin-top:8px;
  font-size:11.5px;color:var(--iris2);cursor:pointer;width:fit-content;font-weight:500;}
.src-toggle svg{transition:transform .18s;}
.src-toggle.open svg{transform:rotate(180deg);}
.src-cards{margin-top:6px;display:flex;flex-direction:column;gap:5px;}
.src-card{display:flex;align-items:center;gap:9px;padding:8px 11px;
  background:var(--ink1);border:1px solid var(--rail);border-radius:10px;cursor:pointer;transition:all .15s;}
.src-card:hover{border-color:var(--iris);background:var(--iris5);}
.src-ico{width:24px;height:24px;background:rgba(240,74,107,0.10);border-radius:6px;
  display:flex;align-items:center;justify-content:center;font-size:11px;flex-shrink:0;}
.src-info{flex:1;min-width:0;}
.src-name{font-size:11.5px;font-weight:500;}
.src-page{font-size:10px;color:var(--ink-3);font-family:var(--mono);margin-top:1px;}
.src-preview{font-size:10.5px;color:var(--ink-3);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:180px;}

/* msg actions */
.msg-meta{display:flex;align-items:center;gap:6px;margin-top:6px;}
.msg-time{font-size:10px;color:var(--ink-3);font-family:var(--mono);}
.copy-btn{padding:3px 9px;border:1px solid var(--rail);border-radius:5px;
  background:transparent;color:var(--ink-3);font-size:10.5px;cursor:pointer;
  transition:all .14s;font-family:var(--font);}
.copy-btn:hover{border-color:var(--rail2);color:var(--ink-2);background:var(--ink2);}
.copy-btn.done{color:var(--jade);border-color:rgba(34,201,160,.3);}

/* ═══ INPUT BAR ══════════════════════════════════════════════════════════════ */

.input-zone{padding:14px 22px 16px;border-top:1px solid var(--rail);background:var(--ink0);flex-shrink:0;}
.no-doc-warn{display:flex;align-items:center;gap:8px;padding:8px 13px;margin-bottom:10px;
  background:var(--sbg);border:1px solid rgba(245,166,35,0.2);border-radius:var(--r);
  font-size:12px;color:var(--sun);}
.input-shell{display:flex;align-items:center;gap:10px;background:var(--ink2);
  border:1px solid var(--rail2);border-radius:14px;padding:10px 14px;
  transition:border-color .2s,box-shadow .2s;}
.input-shell:focus-within{border-color:var(--iris);box-shadow:0 0 0 3px var(--iris4);}
.chat-input{flex:1;background:transparent;border:none;outline:none;
  color:var(--ink);font-family:var(--font);font-size:13.5px;resize:none;}
.chat-input::placeholder{color:var(--ink-4);}
.send-btn{width:34px;height:34px;background:var(--iris);border:none;border-radius:9px;
  display:flex;align-items:center;justify-content:center;cursor:pointer;
  transition:all .18s;flex-shrink:0;}
.send-btn:hover:not(:disabled){background:var(--iris2);transform:scale(1.06);}
.send-btn:active{transform:scale(.98);}
.send-btn:disabled{opacity:.3;cursor:not-allowed;transform:none;}
.input-caption{font-size:10.5px;color:var(--ink-3);text-align:center;margin-top:8px;}
.kbd{background:var(--ink2);border:1px solid var(--rail2);border-radius:4px;
  padding:1px 5px;font-family:var(--mono);font-size:9.5px;}

/* mobile */
.sb-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.6);z-index:199;backdrop-filter:blur(2px);}

@media(max-width:768px){
  .auth-left{display:none;}
  .auth-right{padding:28px 20px;}
  .sidebar{position:fixed;left:0;top:0;bottom:0;z-index:200;transform:translateX(-100%);}
  .sidebar.open{transform:translateX(0);}
  .sb-overlay.open{display:block;}
  .ham-btn{display:flex;}
  .topbar{padding:10px 14px;}
  .msgs-area{padding:16px 14px;}
  .input-zone{padding:10px 14px 12px;}
  .msg-body{max-width:90%;}
}
@media(max-width:400px){
  .auth-form-box{max-width:100%;}
}
`;

/* ─── API base & helpers ───────────────────────────────────────────────────── */
const BASE = "http://localhost:8000";
const API  = BASE + "/api";

const uid  = () => Math.random().toString(36).slice(2, 9);
const ts   = () => new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
const abbr = (n = "") => n.split(" ").map(w => w[0]?.toUpperCase() || "").join("").slice(0, 2) || "U";

async function apiFetch(path, opts = {}, tok = null) {
  const hdrs = { "Content-Type": "application/json", ...(opts.headers || {}) };
  if (tok) hdrs["Authorization"] = "Bearer " + tok;
  try {
    const r = await fetch(BASE + path, { ...opts, headers: hdrs });
    let d; try { d = await r.json(); } catch { d = {}; }
    return { ok: r.ok, status: r.status, data: d };
  } catch (e) {
    return { ok: false, status: 0, data: { detail: e.message } };
  }
}

/* ─── Eye icon ─────────────────────────────────────────────────────────────── */
function Eye({ open }) {
  return open
    ? <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
    : <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><path d="M17.94 17.94A10 10 0 0 1 12 20c-7 0-11-8-11-8a18 18 0 0 1 5.06-5.94M9.9 4.24A9 9 0 0 1 12 4c7 0 11 8 11 8a18 18 0 0 1-2.16 3.19M1 1l22 22"/></svg>;
}

/* ═══ AUTH SCREEN ══════════════════════════════════════════════════════════════ */
function AuthScreen({ onLogin, initResetToken }) {
  const params = new URLSearchParams(window.location.search);
  const [view, setView]     = useState(initResetToken ? "reset" : "login");
  const [tab, setTab]       = useState("login");
  const [f, setF]           = useState({ name: "", email: "", pw: "", newPw: "", newPw2: "" });
  const [showPw, setShowPw] = useState(false);
  const [remember, setRem]  = useState(false);
  const [loading, setLoad]  = useState(false);
  const [err, setErr]       = useState("");
  const [ok, setOk]         = useState("");
  const resetToken = initResetToken || params.get("reset_token") || "";

  const upd = k => e => setF(p => ({ ...p, [k]: e.target.value }));

  useEffect(() => {
    const saved = localStorage.getItem("da_remember");
    if (saved) { setF(p => ({ ...p, email: saved })); setRem(true); }
  }, []);

  async function doLogin() {
    setErr(""); setOk("");
    if (!f.email || !f.pw) { setErr("Please fill in all fields."); return; }
    setLoad(true);
    try {
      const body = new URLSearchParams({ username: f.email, password: f.pw });
      const r = await fetch(`${API}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body,
      });
      const d = await r.json();
      if (r.ok) {
        if (remember) localStorage.setItem("da_remember", f.email);
        else localStorage.removeItem("da_remember");
        onLogin(d.access_token, d.user);
      } else setErr(d.detail || "Invalid credentials.");
    } catch { setErr("Can't reach server — is the backend running?"); }
    finally { setLoad(false); }
  }

  async function doRegister() {
    setErr(""); setOk("");
    if (!f.name.trim()) { setErr("Name is required."); return; }
    if (!f.email || !f.pw) { setErr("Please fill in all fields."); return; }
    if (f.pw.length < 6) { setErr("Password must be at least 6 characters."); return; }
    setLoad(true);
    try {
      const r = await fetch(`${API}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: f.name.trim(), email: f.email, password: f.pw }),
      });
      const d = await r.json();
      if (r.ok) onLogin(d.access_token, d.user);
      else setErr(d.detail || "Registration failed.");
    } catch { setErr("Can't reach server."); }
    finally { setLoad(false); }
  }

  async function doForgot() {
    setErr(""); setOk("");
    if (!f.email) { setErr("Enter your email address."); return; }
    setLoad(true);
    try {
      const r = await fetch(`${API}/auth/forgot-password`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: f.email }),
      });
      const d = await r.json();
      if (r.ok) setOk(d.message);
      else setErr(d.detail || "Request failed.");
    } catch { setErr("Can't reach server."); }
    finally { setLoad(false); }
  }

  async function doReset() {
    setErr(""); setOk("");
    if (!f.newPw || !f.newPw2) { setErr("Please fill in both fields."); return; }
    if (f.newPw.length < 6) { setErr("Password must be at least 6 characters."); return; }
    if (f.newPw !== f.newPw2) { setErr("Passwords don't match."); return; }
    setLoad(true);
    try {
      const r = await fetch(`${API}/auth/reset-password`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token: resetToken, new_password: f.newPw }),
      });
      const d = await r.json();
      if (r.ok) {
        setOk(d.message);
        setTimeout(() => { setView("login"); setOk(""); }, 2500);
      } else setErr(d.detail || "Reset failed.");
    } catch { setErr("Can't reach server."); }
    finally { setLoad(false); }
  }

  const enter = fn => e => { if (e.key === "Enter") fn(); };

  /* forgot view */
  if (view === "forgot") return (
    <div className="auth-root">
      <LeftPanel/>
      <div className="auth-right">
        <div className="auth-form-box">
          <div className="auth-form-title">Forgot password</div>
          <div className="auth-form-sub">Enter your email and we'll send a reset link.</div>
          {err && <div className="auth-err"><Ico type="err"/> {err}</div>}
          {ok  && <div className="auth-ok"><Ico type="ok"/> {ok}</div>}
          {!ok && <>
            <div className="auth-field">
              <label>Email</label>
              <input type="email" value={f.email} onChange={upd("email")}
                placeholder="you@example.com" onKeyDown={enter(doForgot)} autoFocus/>
            </div>
            <button className="auth-submit" onClick={doForgot} disabled={loading}>
              {loading ? "Sending…" : "Send reset link →"}
            </button>
          </>}
          <button className="auth-submit secondary" onClick={() => { setView("login"); setErr(""); setOk(""); }}>
            ← Back to sign in
          </button>
        </div>
      </div>
    </div>
  );

  /* reset view */
  if (view === "reset") return (
    <div className="auth-root">
      <LeftPanel/>
      <div className="auth-right">
        <div className="auth-form-box">
          <div className="auth-form-title">Set new password</div>
          <div className="auth-form-sub">Choose a strong password for your account.</div>
          {err && <div className="auth-err"><Ico type="err"/> {err}</div>}
          {ok  && <div className="auth-ok"><Ico type="ok"/> {ok}</div>}
          {!ok && <>
            <div className="auth-field">
              <label>New password</label>
              <div className="pw-wrap">
                <input type={showPw ? "text" : "password"} value={f.newPw}
                  onChange={upd("newPw")} placeholder="Min 6 characters" autoFocus/>
                <button className="pw-eye" onClick={() => setShowPw(v => !v)} type="button"><Eye open={showPw}/></button>
              </div>
            </div>
            <div className="auth-field">
              <label>Confirm password</label>
              <div className="pw-wrap">
                <input type={showPw ? "text" : "password"} value={f.newPw2}
                  onChange={upd("newPw2")} placeholder="Repeat password" onKeyDown={enter(doReset)}/>
                <button className="pw-eye" onClick={() => setShowPw(v => !v)} type="button"><Eye open={showPw}/></button>
              </div>
            </div>
            <button className="auth-submit" onClick={doReset} disabled={loading}>
              {loading ? "Saving…" : "Update password →"}
            </button>
          </>}
          <button className="auth-submit secondary" onClick={() => { setView("login"); setErr(""); setOk(""); }}>
            ← Back to sign in
          </button>
        </div>
      </div>
    </div>
  );

  /* login / register */
  return (
    <div className="auth-root">
      <LeftPanel/>
      <div className="auth-right">
        <div className="auth-form-box">
          <div className="auth-form-title">{tab === "login" ? "Welcome back" : "Create account"}</div>
          <div className="auth-form-sub">{tab === "login" ? "Sign in to your DOCUAssist account." : "Start querying your documents in minutes."}</div>
          <div className="auth-tabs">
            {["login","signup"].map(t => (
              <div key={t} className={`auth-tab${tab===t?" on":""}`}
                onClick={() => { setTab(t); setErr(""); setOk(""); }}>
                {t === "login" ? "Sign in" : "Create account"}
              </div>
            ))}
          </div>
          {err && <div className="auth-err"><Ico type="err"/> {err}</div>}
          {ok  && <div className="auth-ok"><Ico type="ok"/> {ok}</div>}
          {tab === "signup" && (
            <div className="auth-field">
              <label>Full name</label>
              <input value={f.name} onChange={upd("name")} placeholder="Your name" autoFocus/>
            </div>
          )}
          <div className="auth-field">
            <label>Email</label>
            <input type="email" value={f.email} onChange={upd("email")}
              placeholder="you@example.com" onKeyDown={enter(tab === "login" ? doLogin : doRegister)}
              autoFocus={tab === "login"}/>
          </div>
          <div className="auth-field">
            <label>Password</label>
            <div className="pw-wrap">
              <input type={showPw ? "text" : "password"} value={f.pw}
                onChange={upd("pw")} placeholder="••••••••"
                onKeyDown={enter(tab === "login" ? doLogin : doRegister)}/>
              <button className="pw-eye" onClick={() => setShowPw(v => !v)} type="button"><Eye open={showPw}/></button>
            </div>
          </div>
          {tab === "login" && (
            <div className="auth-meta">
              <label className="auth-remember">
                <input type="checkbox" checked={remember} onChange={e => setRem(e.target.checked)}/>
                <span>Remember me</span>
              </label>
              <button className="auth-forgot" onClick={() => { setView("forgot"); setErr(""); setOk(""); }}>
                Forgot password?
              </button>
            </div>
          )}
          <button className="auth-submit" onClick={tab === "login" ? doLogin : doRegister} disabled={loading}>
            {loading ? "Please wait…" : tab === "login" ? "Sign in →" : "Create account →"}
          </button>
          <div className="auth-hint">
            {tab === "login" ? "No account? " : "Have an account? "}
            <b onClick={() => { setTab(tab === "login" ? "signup" : "login"); setErr(""); setOk(""); }}>
              {tab === "login" ? "Sign up free" : "Sign in"}
            </b>
          </div>
        </div>
      </div>
    </div>
  );
}

/* decorative left panel (reused across auth views) */
function LeftPanel() {
  return (
    <div className="auth-left">
      <div className="auth-left-glow"/>
      <div className="auth-left-glow2"/>
      <div className="auth-wordmark">
        <div className="auth-logo">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
            <line x1="16" y1="13" x2="8" y2="13"/>
            <line x1="16" y1="17" x2="8" y2="17"/>
            <polyline points="10 9 9 9 8 9"/>
          </svg>
        </div>
        <span className="auth-wordmark-text">DOCU<em>Assist</em></span>
      </div>
      <div className="auth-hero">
        <div className="auth-tagline">Ask anything about<br/><em>your documents</em></div>
        <div className="auth-desc">Upload PDFs and get instant, sourced answers powered by RAG — no hallucinations, no guesswork.</div>
        <div className="auth-pills">
        </div>
      </div>
      <div className="auth-footer-txt">DOCUAssist · AI document intelligence</div>
    </div>
  );
}

/* tiny icon helpers */
function Ico({ type }) {
  if (type === "err") return <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>;
  return <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"><polyline points="20 6 9 17 4 12"/></svg>;
}

/* ═══ MESSAGE COMPONENT ════════════════════════════════════════════════════════ */
function Message({ msg, userInits }) {
  const isBot = msg.role === "assistant";
  const [srcOpen, setSrc] = useState(false);
  const [copied, setCopy] = useState(false);

  function copy() {
    navigator.clipboard?.writeText(msg.content);
    setCopy(true);
    setTimeout(() => setCopy(false), 1800);
  }

  const lines = (msg.content || "").split("\n");

  function renderLine(line, i) {
    if (!line) return <div key={i} style={{ height: 6 }}/>;
    const html = line
      .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
      .replace(/`(.+?)`/g, `<code>$1</code>`);
    if (/^[•\-]\s/.test(line)) {
      return (
        <div key={i} style={{ display:"flex", gap:8, alignItems:"flex-start", marginBottom:3 }}>
          <span style={{ color:"var(--iris3)", marginTop:3, flexShrink:0, fontSize:12 }}>▸</span>
          <span dangerouslySetInnerHTML={{ __html: html.replace(/^[•\-]\s/,"") }}/>
        </div>
      );
    }
    return <div key={i} dangerouslySetInnerHTML={{ __html: html }}/>;
  }

  return (
    <div className={`msg${isBot ? "" : " user"}`}>
      <div className={`msg-avatar${isBot ? " bot" : " usr"}`}>
        {isBot
          ? <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.2" strokeLinecap="round"><rect x="3" y="10" width="18" height="11" rx="3"/><path d="M7 10V7a5 5 0 0 1 10 0v3"/><circle cx="9" cy="16" r="1" fill="white" stroke="none"/><circle cx="15" cy="16" r="1" fill="white" stroke="none"/></svg>
          : userInits}
      </div>
      <div className="msg-body">
        {msg.typing
          ? <div className="bubble bot"><div className="typing-dots"><div className="dot"/><div className="dot"/><div className="dot"/></div></div>
          : <>
            <div className={`bubble${isBot ? " bot" : " user"}`}>
              {lines.map(renderLine)}
            </div>

            {isBot && msg.sources?.length > 0 && (
              <>
                <div className={`src-toggle${srcOpen?" open":""}`} onClick={() => setSrc(o => !o)}>
                  <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"><path d="M6 9l6 6 6-6"/></svg>
                  {msg.sources.length} source{msg.sources.length > 1 ? "s" : ""}
                </div>
                {srcOpen && (
                  <div className="src-cards">
                    {msg.sources.map((s, i) => (
                      <div className="src-card" key={i}>
                        <div className="src-ico">📄</div>
                        <div className="src-info">
                          <div className="src-name">{s.filename}</div>
                          <div className="src-page">p. {s.page}</div>
                        </div>
                        <div className="src-preview">{s.preview}</div>
                      </div>
                    ))}
                  </div>
                )}
              </>
            )}

            <div className="msg-meta">
              <span className="msg-time">{msg.time}</span>
              {isBot && (
                <button className={`copy-btn${copied?" done":""}`} onClick={copy}>
                  {copied ? "✓ Copied" : "Copy"}
                </button>
              )}
            </div>
          </>
        }
      </div>
    </div>
  );
}

/* ═══ DELETE MODAL ══════════════════════════════════════════════════════════════ */
function DeleteModal({ doc, onConfirm, onCancel, busy }) {
  return (
    <div className="modal-veil" onClick={onCancel}>
      <div className="modal-box" onClick={e => e.stopPropagation()}>
        <div className="modal-title">Delete document?</div>
        <div className="modal-body">
          <strong>{doc.name}</strong> will be permanently removed along with its vector index.
          This can't be undone.
        </div>
        <div className="modal-btns">
          <button className="modal-cancel" onClick={onCancel} disabled={busy}>Cancel</button>
          <button className="modal-delete" onClick={onConfirm} disabled={busy}>
            {busy ? "Deleting…" : "Delete"}
          </button>
        </div>
      </div>
    </div>
  );
}

/* ═══ MAIN APP ══════════════════════════════════════════════════════════════════ */
export default function App() {
  const urlParams = new URLSearchParams(window.location.search);
  const initReset = urlParams.get("reset_token") || "";

  const [token, setToken]     = useState(() => localStorage.getItem("da_token"));
  const [user, setUser]       = useState(() => { try { return JSON.parse(localStorage.getItem("da_user")||"null"); } catch { return null; } });
  const [chats, setChats]     = useState([]);
  const [chatId, setChatId]   = useState(null);
  const [msgs, setMsgs]       = useState([]);
  const [docs, setDocs]       = useState([]);
  const [activeDocs, setAD]   = useState([]);
  const [showUp, setShowUp]   = useState(false);
  const [uploading, setUpl]   = useState(false);
  const [uplFile, setUplFile] = useState("");
  const [uplResult, setUplR]  = useState(null); // { ok, text }
  const [dragging, setDrag]   = useState(false);
  const [question, setQ]      = useState("");
  const [busy, setBusy]       = useState(false);
  const [sideOpen, setSide]   = useState(false);
  const [loadHist, setLoadH]  = useState(false);
  const [delDoc, setDelDoc]   = useState(null);
  const [delBusy, setDelBusy] = useState(false);

  const fileRef = useRef(null);
  const msgsRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => { if (msgsRef.current) msgsRef.current.scrollTop = msgsRef.current.scrollHeight; }, [msgs]);

  useEffect(() => {
    if (token) localStorage.setItem("da_token", token); else localStorage.removeItem("da_token");
  }, [token]);
  useEffect(() => {
    if (user) localStorage.setItem("da_user", JSON.stringify(user)); else localStorage.removeItem("da_user");
  }, [user]);

  useEffect(() => { if (token) loadInit(token); }, []);

  useEffect(() => {
    function onKey(e) { if ((e.ctrlKey||e.metaKey) && e.key==="k") { e.preventDefault(); inputRef.current?.focus(); } }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  async function loadInit(tok) {
    const [cr, dr] = await Promise.all([apiFetch("/api/chats",{},tok), apiFetch("/api/documents",{},tok)]);
    if (cr.ok) setChats(cr.data); else if (cr.status===401) { logout(); return; }
    if (dr.ok) { setDocs(dr.data); setAD(dr.data.map(d=>d.id)); }
  }

  function login(tok, usr) {
    setToken(tok); setUser(usr);
    if (initReset) window.history.replaceState({}, "", window.location.pathname);
    loadInit(tok);
  }

  function logout() {
    setToken(null); setUser(null); setChats([]); setMsgs([]); setDocs([]); setAD([]); setChatId(null);
    localStorage.removeItem("da_token"); localStorage.removeItem("da_user");
  }

  async function newChat() {
    const { ok, data } = await apiFetch("/api/chats",{method:"POST",body:"{}"},token);
    if (ok) { setChats(p=>[data,...p]); setChatId(data.id); setMsgs([]); setSide(false); }
  }

  async function openChat(id) {
    if (id===chatId) { setSide(false); return; }
    setLoadH(true); setChatId(id); setMsgs([]);
    const { ok, data } = await apiFetch(`/api/chats/${id}/messages`,{},token);
    if (ok) setMsgs(data.map(m=>({...m,time:""})));
    setLoadH(false); setSide(false);
  }

  async function delChat(id) {
    await apiFetch(`/api/chats/${id}`,{method:"DELETE"},token);
    setChats(p=>p.filter(c=>c.id!==id));
    if (chatId===id) { setChatId(null); setMsgs([]); }
  }

  function toggleDoc(id) { setAD(p=>p.includes(id)?p.filter(x=>x!==id):[...p,id]); }

  async function confirmDel() {
    setDelBusy(true);
    await apiFetch(`/api/documents/${delDoc.id}`,{method:"DELETE"},token);
    setDocs(p=>p.filter(d=>d.id!==delDoc.id));
    setAD(p=>p.filter(x=>x!==delDoc.id));
    setDelBusy(false); setDelDoc(null);
  }

  async function handleFile(file) {
    if (!file || !file.name.toLowerCase().endsWith(".pdf")) {
      setUplR({ ok:false, text:"Only PDF files are supported." }); return;
    }
    setUpl(true); setUplFile(file.name); setUplR(null);
    try {
      const fd = new FormData(); fd.append("file", file);
      const r = await fetch(`${API}/upload`,{method:"POST",headers:{Authorization:"Bearer "+token},body:fd});
      const d = await r.json();
      if (!r.ok) throw new Error(d.detail||"Upload failed");
      const doc = { id:d.doc_id||d.id, name:d.name||d.filename, pages:d.pages, chunks:d.chunks };
      setDocs(p=>[doc,...p]); setAD(p=>[doc.id,...p]);
      setUplR({ ok:true, text:`✓ ${doc.name} — ${doc.pages} pages, ${doc.chunks} chunks indexed` });
    } catch(e) { setUplR({ ok:false, text:`Upload failed: ${e.message}` }); }
    finally { setUpl(false); }
  }

  async function ask() {
    if (!question.trim()||busy||!activeDocs.length) return;
    const q = question.trim(); setQ(""); setBusy(true);
    const uMsg = { id:uid(), role:"user", content:q, time:ts(), sources:[] };
    const tMsg = { id:uid(), role:"assistant", content:"", typing:true, time:ts() };
    setMsgs(p=>[...p,uMsg,tMsg]);
    try {
      const r = await fetch(`${API}/ask`,{
        method:"POST",
        headers:{"Content-Type":"application/json","Authorization":"Bearer "+token},
        body:JSON.stringify({question:q,doc_ids:activeDocs,chat_id:chatId??null}),
      });
      const d = await r.json();
      setMsgs(p=>{
        const clean = p.filter(m=>!m.typing);
        return [...clean,{id:uid(),role:"assistant",content:r.ok?d.answer:`Error: ${d.detail||"Query failed"}`,sources:r.ok?(d.sources||[]):[],time:ts()}];
      });
      if (d.chat_id) {
        setChatId(d.chat_id);
        setChats(p=>{
          const ex=p.find(c=>c.id===d.chat_id);
          if(ex) return p.map(c=>c.id===d.chat_id?{...c,title:c.title==="New conversation"?q.slice(0,52):c.title}:c);
          return [{id:d.chat_id,title:q.slice(0,52)},...p];
        });
      }
    } catch {
      setMsgs(p=>[...p.filter(m=>!m.typing),{id:uid(),role:"assistant",content:"Server error — check if the backend is running.",sources:[],time:ts()}]);
    } finally { setBusy(false); }
  }

  const SUGGESTIONS = [
    "What is the main topic of this document?",
    "Summarize the key findings",
    "What dates or deadlines are mentioned?",
    "List the main recommendations",
  ];

  if (!token || initReset) {
    return <><style>{CSS}</style><AuthScreen onLogin={login} initResetToken={initReset}/></>;
  }

  const inits = abbr(user?.name);

  return (
    <>
      <style>{CSS}</style>
      {delDoc && <DeleteModal doc={delDoc} onConfirm={confirmDel} onCancel={()=>setDelDoc(null)} busy={delBusy}/>}

      <div className="app">
        {/* sidebar overlay mobile */}
        <div className={`sb-overlay${sideOpen?" open":""}`} onClick={()=>setSide(false)}/>

        {/* ── SIDEBAR ── */}
        <div className={`sidebar${sideOpen?" open":""}`}>
          <div className="sb-top">
            <div className="sb-logo">
              <div className="sb-logo-icon">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.2" strokeLinecap="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                </svg>
              </div>
              <span className="sb-logo-name">DOCU<em>Assist</em></span>
            </div>
            <button className="new-chat-btn" onClick={newChat}>
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
              New conversation
            </button>
          </div>

          <div className="hist-body">
            {chats.length === 0
              ? <div className="hist-none">No conversations yet.<br/>Upload a PDF and start asking.</div>
              : <>
                  <div className="hist-group-lbl">Recent</div>
                  {chats.map(c => (
                    <div key={c.id} className={`hist-row${c.id===chatId?" active":""}`} onClick={()=>openChat(c.id)}>
                      <svg className="hist-row-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
                      <span className="hist-row-txt">{c.title||"New conversation"}</span>
                      <button className="hist-del-btn" onClick={e=>{e.stopPropagation();delChat(c.id);}}>
                        <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                      </button>
                    </div>
                  ))}
                </>
            }
          </div>

          <div className="sb-bottom">
            <div className="user-row">
              <div className="user-av">{inits}</div>
              <div className="user-details">
                <div className="user-name">{user?.name||"User"}</div>
                <div className="user-email">{user?.email}</div>
              </div>
              <button className="signout-btn" onClick={logout} title="Sign out">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>
                </svg>
              </button>
            </div>
          </div>
        </div>

        {/* ── MAIN ── */}
        <div className="main">

          {/* topbar */}
          <div className="topbar">
            <div className="topbar-left">
              <button className="ham-btn" onClick={()=>setSide(o=>!o)}>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
              </button>
              <div>
                <div className="chat-title">Document Intelligence</div>
                <div className="chat-sub">Sourced answers from your PDFs</div>
              </div>
            </div>
            <button className="upload-btn" onClick={()=>{setShowUp(o=>!o);setUplR(null);}}>
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/>
              </svg>
              Upload PDF
              {docs.length > 0 && <span className="doc-count-badge">{docs.length}</span>}
            </button>
          </div>

          {/* upload drawer */}
          {showUp && (
            <div className="upload-drawer">
              <div
                className={`dropzone${dragging?" over":""}`}
                onClick={()=>fileRef.current?.click()}
                onDragOver={e=>{e.preventDefault();setDrag(true);}}
                onDragLeave={()=>setDrag(false)}
                onDrop={e=>{e.preventDefault();setDrag(false);handleFile(e.dataTransfer.files[0]);}}
              >
                <div className="dz-icon">☁</div>
                <div className="dz-txt">Drag & drop a PDF here — or <b>click to browse</b></div>
                <input ref={fileRef} type="file" accept=".pdf" style={{display:"none"}}
                  onChange={e=>{handleFile(e.target.files[0]);e.target.value="";}}/>
              </div>
              {uploading && (
                <div className="upload-progress">
                  <div className="spinner"/>
                  <span className="upload-fname">Processing {uplFile}…</span>
                </div>
              )}
              {uplResult && (
                <div className={`upload-result${uplResult.ok?" ok":" err"}`}>{uplResult.text}</div>
              )}
              {docs.length > 0 && (
                <div className="doc-lib">
                  <div className="doc-lib-hdr">
                    <span className="doc-lib-label">{activeDocs.length}/{docs.length} active</span>
                    <div className="doc-ctrl-row">
                      <button className="doc-ctrl-btn" onClick={()=>setAD(docs.map(d=>d.id))}>All</button>
                      <button className="doc-ctrl-btn" onClick={()=>setAD([])}>None</button>
                    </div>
                  </div>
                  <div className="doc-chips">
                    {docs.map(d => {
                      const on = activeDocs.includes(d.id);
                      return (
                        <div key={d.id} className={`doc-chip${on?" active":""}`} onClick={()=>toggleDoc(d.id)}>
                          <div className="doc-chip-dot"/>
                          <span className="doc-chip-name">{d.name}</span>
                          <span className="doc-chip-pg">{d.pages}p</span>
                          <button className="doc-chip-del" title="Delete"
                            onClick={e=>{e.stopPropagation();setDelDoc(d);}}>
                            <svg width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
                              <polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>
                              <path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/>
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

          {/* messages */}
          <div className="msgs-area" ref={msgsRef}>
            {loadHist
              ? <div className="welcome"><div className="spinner" style={{width:22,height:22,borderWidth:3}}/></div>
              : msgs.length === 0
                ? <div className="welcome">
                    <div className="welcome-orb">
                      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--iris3)" strokeWidth="1.8" strokeLinecap="round">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                        <polyline points="14 2 14 8 20 8"/>
                        <line x1="16" y1="13" x2="8" y2="13"/>
                        <line x1="16" y1="17" x2="8" y2="17"/>
                      </svg>
                    </div>
                    <div className="welcome-title">
                      {docs.length === 0 ? `Hey ${user?.name?.split(" ")[0]||"there"} 👋` : `${docs.length} doc${docs.length>1?"s":""} ready`}
                    </div>
                    <div className="welcome-sub">
                      {docs.length === 0
                        ? "Upload a PDF above, then ask anything about its content."
                        : "Ask a question about your uploaded documents."}
                    </div>
                    {docs.length > 0 && (
                      <div className="sug-row">
                        {SUGGESTIONS.map(s => (
                          <button key={s} className="sug-btn"
                            onClick={()=>{ if (!activeDocs.length) return; setQ(s); inputRef.current?.focus(); }}>
                            {s}
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                : msgs.map(m => <Message key={m.id} msg={m} userInits={inits}/>)
            }
          </div>

          {/* input */}
          <div className="input-zone">
            {activeDocs.length === 0 && docs.length > 0 && (
              <div className="no-doc-warn">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
                No documents selected — open Upload PDF to select one.
              </div>
            )}
            <div className="input-shell">
              <input
                ref={inputRef}
                className="chat-input"
                value={question}
                onChange={e=>setQ(e.target.value)}
                onKeyDown={e=>e.key==="Enter"&&!e.shiftKey&&ask()}
                placeholder={activeDocs.length ? "Ask anything about your documents…" : "Upload a PDF first…"}
                disabled={busy}
              />
              <button className="send-btn" onClick={ask}
                disabled={!question.trim()||busy||!activeDocs.length}>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                  <path d="M22 2L11 13" stroke="white" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"/>
                  <path d="M22 2L15 22 11 13 2 9l20-7z" stroke="white" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </button>
            </div>
            <div className="input-caption">
              <span className="kbd">Enter</span> to send · <span className="kbd">⌘K</span> focus · RAG · FAISS · Gemini
            </div>
          </div>

        </div>
      </div>
    </>
  );
}