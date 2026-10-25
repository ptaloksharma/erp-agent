"""erp-agent — Routes enterprise ERP user requests securely down the mesh and delegates domain tasks to specialized agents. (scaffolded by Buddy interactive wizard).

Guardrail profile: standard
Compliance packs : bola,gdpr
Telemetry        : stdout
Cloud target     : azure
Pipeline         : github
Requirements     : pasted in chat
"""
# REQUIREMENTS.md (fetched from your spec URL) is the source of truth for
# this agent's business logic. Read it before extending the tools below.
import io, os, sys, time
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
# --- dm-agent-kit path bootstrap (v3.48.2) ------------------------------
# The agent lives in the consumer workspace; the governance libraries live
# in the installed kit (node_modules/dm-agent-kit/dist/src) or a local
# kit checkout (dm-agent-kit/src). Walk up from this file to find either.
def _bootstrap_kit_path():
    here = os.path.dirname(os.path.abspath(__file__))
    env_root = os.environ.get("DM_AGENT_KIT_ROOT")
    cands = []
    if env_root:
        cands += [os.path.join(env_root, "dist", "src"), os.path.join(env_root, "src")]
    d = here
    for _ in range(8):
        cands.append(os.path.join(d, "node_modules", "dm-agent-kit", "dist", "src"))
        cands.append(os.path.join(d, "dm-agent-kit", "src"))
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    for c in cands:
        if os.path.isdir(os.path.join(c, "dm_agent_sec")):
            if c not in sys.path:
                sys.path.insert(0, c)
            return
_bootstrap_kit_path()
import jwt
from dm_agent_sec.core.auth_context import JWTVerifier
from dm_agent_sec.core.ports import InMemoryOwnership
from dm_agent_sec.diagnostics.friendly_police import FriendlyPolice
from dm_agent_sec.langgraph.governor import GraphExecutionGovernor
from dm_agent_kit.plugins.security_bridge import DshSecurityBridge
from dm_agent_kit.plugins.friendly_police_observer import FriendlyPoliceObserver

SECRET = os.environ.get("SECURI_DEV_SECRET", "securi-dev-only-secret-key-32-bytes!")
WORKDIR = os.path.dirname(os.path.abspath(__file__))
STRICTNESS = "standard"
COMPLIANCE = ["bola", "gdpr"]
TELEMETRY = ["stdout"]

def make_auth():
    now = int(time.time())
    token = jwt.encode({"sub": "erp-agent", "tenant_id": "tenant-1",
                        "customer_id": "cust-dev", "roles": ["operator"],
                        "scope": "read write", "iat": now, "exp": now + 3600},
                       SECRET, algorithm="HS256")
    return JWTVerifier(secret=SECRET).verify(token)

def build_stack():
    auth = make_auth()
    governor = GraphExecutionGovernor(
        max_steps=15 if STRICTNESS != "strict" else 8,
        max_tokens=100_000 if STRICTNESS != "strict" else 40_000)
    bridge = DshSecurityBridge(
        auth=auth,
        ownership=InMemoryOwnership(),
        governor=governor,
    )
    copilot = FriendlyPolice()
    observer = FriendlyPoliceObserver(bridge, workdir=WORKDIR, copilot=copilot).attach()
    return bridge, copilot, observer

from ui_contract import UIContractAdapter


def run():
    bridge, copilot, observer = build_stack()

    def echo(message: str) -> str:
        """Sample tool — replace with your Routes enterprise ERP user requests securely down the mesh and delegates domain tasks to specialized agents. logic."""
        return f"[erp-agent] guarded reply: {message}"

    guarded = bridge.wrap_tool("echo", echo)
    print("🌷 erp-agent is alive (profile: standard, packs: bola,gdpr)")
    _adapter = UIContractAdapter('erp-agent')
    print(_adapter.dumps(_adapter.wrap(guarded(message="hello from Buddy"))))

    # v3.48.8: execute the real business workflow (src/logic/workflow.py)
    # through the governed bridge — agent.py is no longer a dummy echo.
    import importlib.util as _ilu
    _wf_path = os.path.join(WORKDIR, "src", "logic", "workflow.py")
    if os.path.exists(_wf_path):
        _logic_dir = os.path.dirname(_wf_path)
        _pkg = "_logic_" + "erp-agent".replace("-", "_")
        _init = os.path.join(_logic_dir, "__init__.py")
        _pspec = _ilu.spec_from_file_location(
            _pkg, _init if os.path.exists(_init) else _wf_path,
            submodule_search_locations=[_logic_dir])
        if _pspec and _pspec.loader:
            _pm = _ilu.module_from_spec(_pspec)
            sys.modules[_pkg] = _pm
            if os.path.exists(_init):
                _pspec.loader.exec_module(_pm)
        # v3.48.10: load tools.py as <pkg>.tools and store each WRAPPED
        # tool back into TOOLS in-place — workflow.py's relative
        # `from .tools import TOOLS` resolves to this exact dict, so every
        # TOOLS["..."](input) call inside workflow.run crosses the
        # DshSecurityBridge (previously wrap_tool's return was dropped
        # and workflow ran the RAW, unguarded functions).
        _t_path = os.path.join(_logic_dir, "tools.py")
        if os.path.exists(_t_path):
            _tspec = _ilu.spec_from_file_location(_pkg + ".tools", _t_path)
            if _tspec and _tspec.loader:
                _tm = _ilu.module_from_spec(_tspec)
                sys.modules[_pkg + ".tools"] = _tm
                _tspec.loader.exec_module(_tm)
                for _tname, _tfn in list(getattr(_tm, "TOOLS", {}).items()):
                    if _tname == "echo":
                        continue
                    _guarded = bridge.wrap_tool(
                        _tname, (lambda fn: lambda **kw: fn(kw))(_tfn))
                    # adapt: workflow calls TOOLS[x](payload_dict)
                    _tm.TOOLS[_tname] = (lambda g: lambda payload=None, **kw:
                        g(**(payload if isinstance(payload, dict) else kw)))(_guarded)
        _spec = _ilu.spec_from_file_location(_pkg + ".workflow", _wf_path)
        if _spec and _spec.loader:
            _wf = _ilu.module_from_spec(_spec)
            sys.modules[_pkg + ".workflow"] = _wf
            _spec.loader.exec_module(_wf)
            if hasattr(_wf, "run"):
                _out = _wf.run({"message": "hello from Buddy", "tenant_id": "tenant-1"})
                print(f"🧠 workflow.run → {_out}")

    # v3.48.8: a ui-coordinator demonstrates a REAL governed vertical
    # handoff — discovers registered domain-agents in erp-mesh-registry.json
    # and delegates across the DSH mesh bridge (4 mandatory checks + audit).
    if STRICTNESS is not None and "ui-coordinator" == "ui-coordinator":
        try:
            import mesh_bridge as _mb
            import json as _json
            _root = _mb._workspace_root(WORKDIR)
            _reg = _mb._load_registry(_root)
            _targets = [a["name"] for a in _reg.get("agents", [])
                        if a.get("role") == "domain-agent" and a["name"] != "erp-agent"]
            if _targets:
                _res = _mb.delegate_to_agent(
                    _targets[0],
                    {"invoice_id": "INV-DEMO-001", "amount": 1200},
                    task="demo vertical handoff",
                    tenant_id="tenant-1")
                print(f"🕸️  governed handoff erp-agent → {_targets[0]}:")
                print("   trace:", _json.dumps(_res["trace"], indent=2))
                print("   result:", _res["result"])
            else:
                print("🕸️  no domain-agent registered yet — scaffold one, then re-run for the live handoff")
        except Exception as _he:
            print(f"🕸️  handoff skipped ({type(_he).__name__}: {_he})")
    observer.flush()

def mesh_test():
    """v3.48.11: adversarial mesh security chaos runner (ui-coordinator only).

    4 live verification vectors across the registered mesh; prints a
    PASS/BLOCK compliance table; exit 0 only when all 4 behave as expected.
    """
    import json as _j
    rows = []
    def _row(vec, expect, ok, detail):
        rows.append((vec, expect, "PASS" if ok else "FAIL", detail))
        return ok
    try:
        import mesh_bridge as _mb
    except Exception as e:
        print(f"MESH-TEST FAIL (mesh_bridge unavailable: {e})")
        return 1
    _root = _mb._workspace_root(WORKDIR)
    _reg = _mb._load_registry(_root)
    _targets = [a["name"] for a in _reg.get("agents", [])
                if a.get("role") == "domain-agent" and a["name"] != "erp-agent"]
    if not _targets:
        print("MESH-TEST FAIL (no domain-agent registered — scaffold one first)")
        return 1
    _t = _targets[0]

    # Vector 1 — valid touchless handoff (amount 1200, tenant-1)
    try:
        r1 = _mb.delegate_to_agent(_t, {"invoice_id": "INV-TEST-001", "amount": 1200},
                                   task="mesh-test v1", tenant_id="tenant-1")
        _res = r1.get("result") or {}
        _tools = (_res.get("results") or {}).keys()
        ok1 = (r1["trace"].get("audit_chain_valid") is True
               and _res.get("verdict") in ("ALLOW", None)
               and len([t for t in _tools if t != "delegate_to_sub_agent"]) >= 1)
        _row("V1 valid handoff (€1,200)", "ALLOW + tools + chain-valid", ok1,
             f"verdict={_res.get('verdict', 'n/a')} tools={sorted(_tools)}")
    except Exception as e:
        _row("V1 valid handoff (€1,200)", "ALLOW + tools + chain-valid", False,
             f"{type(e).__name__}: {e}"); ok1 = False

    # Vector 2 — high-value DoA spend gate (amount 30000)
    try:
        r2 = _mb.delegate_to_agent(_t, {"invoice_id": "INV-TEST-002", "amount": 30000},
                                   task="mesh-test v2", tenant_id="tenant-1")
        _res2 = r2.get("result") or {}
        _posted = (_res2.get("results") or {}).get("post_invoice")
        ok2 = (_res2.get("verdict") == "SUSPEND_FOR_HITL" and _posted is None)
        _row("V2 DoA gate (€30,000)", "SUSPEND_FOR_HITL, no post", ok2,
             f"verdict={_res2.get('verdict', 'n/a')} post_invoice={'posted' if _posted else 'skipped'}")
    except Exception as e:
        _row("V2 DoA gate (€30,000)", "SUSPEND_FOR_HITL, no post", False,
             f"{type(e).__name__}: {e}"); ok2 = False

    # Vector 3 — cross-tenant BOLA attack
    try:
        from dm_agent_sec.core.auth_context import JWTVerifier as _JV
        import jwt as _jwt, time as _time
        _tok = _jwt.encode({"sub": "erp-agent", "tenant_id": "tenant-1",
                            "customer_id": "cust-dev", "roles": ["operator"],
                            "scope": "read write",
                            "iat": int(_time.time()), "exp": int(_time.time()) + 3600},
                           SECRET, algorithm="HS256")
        _auth = _JV(secret=SECRET).verify(_tok)
        try:
            _mb.delegate_to_agent(_t, {"invoice_id": "INV-TEST-003", "amount": 50},
                                  task="mesh-test v3", auth=_auth, tenant_id="tenant-2")
            ok3 = False; _d3 = "no exception — BOLA bypass!"
        except Exception as e3:
            ok3 = ("SECURI-MESH-BOLA" in str(e3) or "BOLA" in type(e3).__name__
                   or "SECURI-MESH-BOLA" in getattr(e3, "code", ""))
            _d3 = f"{type(e3).__name__}: {str(e3)[:80]}"
        _row("V3 cross-tenant BOLA", "HandoffDenied(SECURI-MESH-BOLA)", ok3, _d3)
    except Exception as e:
        _row("V3 cross-tenant BOLA", "HandoffDenied(SECURI-MESH-BOLA)", False,
             f"setup: {e}"); ok3 = False

    # Vector 4 — unauthorized caller / role bypass (direct target call to a
    # non-existent target violates registry; and a rogue target violates
    # allowedTargets contract)
    try:
        try:
            _mb.delegate_to_agent("rogue-agent", {"amount": 10},
                                  task="mesh-test v4", tenant_id="tenant-1")
            ok4 = False; _d4 = "no exception — delegation bypass!"
        except Exception as e4:
            ok4 = any(c in str(e4) for c in
                      ("SECURI-MESH-UNKNOWN", "SECURI-MESH-DELEGATION", "SECURI-MESH-CALLER"))
            _d4 = f"{type(e4).__name__}: {str(e4)[:80]}"
        _row("V4 unauthorized delegation", "HandoffDenied(UNKNOWN/DELEGATION)", ok4, _d4)
    except Exception as e:
        _row("V4 unauthorized delegation", "HandoffDenied(UNKNOWN/DELEGATION)", False,
             f"setup: {e}"); ok4 = False

    print(chr(10) + "🕸️  MESH SECURITY CHAOS TEST — compliance table")
    print("┌────────────────────────────────┬──────────────────────────────────┬────────┐")
    for vec, expect, status, detail in rows:
        print(f"│ {vec:<30} │ {status:<6} │ {detail[:60]:<60}")
    print("└────────────────────────────────┴──────────────────────────────────┴────────┘")
    passed = sum(1 for r in rows if r[2] == "PASS")
    if passed == 4:
        print("MESH-TEST PASS (4/4 vectors verified)")
        return 0
    print(f"MESH-TEST FAIL ({passed}/4 vectors verified)")
    return 1

if __name__ == "__main__":
    import sys as _sys
    if "--mesh-test" in _sys.argv:
        _sys.exit(mesh_test())
    if "--self-test" in _sys.argv:
        _b, _c, _o = build_stack()
        def _echo(message):
            return f"[self] guarded reply: {message}"
        _g = _b.wrap_tool("echo", _echo)
        assert "guarded reply" in str(_g(message="self-test")), "guarded path failed"
        # architecture drift check: GOAL.yaml intent vs actual code
        try:
            import os as _o2, sys as _s2
            _cands = [
                _o2.environ.get("DM_AGENT_KIT_SRC"),
                _o2.path.join(_o2.path.dirname(__file__), "..", "..", "src"),
                _o2.path.join(_o2.path.dirname(__file__), "..", "src"),
                _o2.path.join(_o2.getcwd(), "src"),
                _o2.path.join(_o2.getcwd(), "..", "src"),
                _o2.path.join(_o2.getcwd(), "..", "..", "src"),
            ]
            for _c in _cands:
                if _c and _o2.path.isdir(_o2.path.join(_c, "buddy")):
                    _s2.path.insert(0, _o2.path.join(_c, "buddy"))
                    break
            from drift import detect_drift as _detect_drift
            _d = _detect_drift(_o2.path.dirname(_o2.path.abspath(__file__)))
            if _d:
                print("⚠️ " + _d["message"])
                print("   Resolve: securi reconfigure --to-single  (or chat: 'convert to single agent')")
                _sys.exit(1)
        except ImportError:
            pass
        print("SELF-TEST PASS")
        _sys.exit(0)
    run()
