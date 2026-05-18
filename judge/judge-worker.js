const PYODIDE_INDEX_URL = "https://cdn.jsdelivr.net/pyodide/v0.27.5/full/";
const BROWSERCC_URL = "https://cdn.jsdelivr.net/npm/browsercc@0.1.1/dist/index.js";
const WASI_SHIM_URL = "https://cdn.jsdelivr.net/npm/@bjorn3/browser_wasi_shim@0.4.2/dist/index.js";

let pyodideReady = null;
let cppRuntimeReady = null;
let cppProgramIdCounter = 1;
const cppPrograms = new Map();

async function ensurePyodide() {
  if (!pyodideReady) {
    pyodideReady = (async () => {
      importScripts(`${PYODIDE_INDEX_URL}pyodide.js`);
      const pyodide = await self.loadPyodide({ indexURL: PYODIDE_INDEX_URL });
      return pyodide;
    })();
  }
  return pyodideReady;
}

async function ensureCppRuntime() {
  if (!cppRuntimeReady) {
    cppRuntimeReady = (async () => {
      const [browserccMod, wasiShimMod] = await Promise.all([
        import(BROWSERCC_URL),
        import(WASI_SHIM_URL),
      ]);
      if (typeof browserccMod.compile !== "function") {
        throw new Error("browsercc compile() is unavailable");
      }
      return {
        compile: browserccMod.compile,
        WASI: wasiShimMod.WASI,
        File: wasiShimMod.File,
        OpenFile: wasiShimMod.OpenFile,
        ConsoleStdout: wasiShimMod.ConsoleStdout,
      };
    })();
  }
  return cppRuntimeReady;
}

async function runPython(code, inputData) {
  const pyodide = await ensurePyodide();
  const wrapper = `
import io
import json
import sys
import traceback

_submission_code = ${JSON.stringify(code)}
_submission_input = ${JSON.stringify(inputData)}
_stdout = io.StringIO()
_stderr = io.StringIO()
_old_stdin, _old_stdout, _old_stderr = sys.stdin, sys.stdout, sys.stderr
sys.stdin = io.StringIO(_submission_input)
sys.stdout = _stdout
sys.stderr = _stderr
_exit_code = 0
_error = ""

try:
    _globals = {"__name__": "__main__", "__file__": "<submission>"}
    exec(compile(_submission_code, "<submission>", "exec"), _globals, _globals)
except SystemExit as _exc:
    if _exc.code not in (None, 0):
        _exit_code = 1
        _error = f"SystemExit: {_exc.code}"
except Exception:
    _exit_code = 1
    _error = traceback.format_exc()
finally:
    sys.stdin, sys.stdout, sys.stderr = _old_stdin, _old_stdout, _old_stderr

_judge_result = json.dumps({
    "stdout": _stdout.getvalue(),
    "stderr": _stderr.getvalue(),
    "exit_code": _exit_code,
    "error": _error,
})
`;

  await pyodide.runPythonAsync(wrapper);
  const resultJson = pyodide.runPython("_judge_result");
  return JSON.parse(resultJson);
}

async function compileCpp(code) {
  const runtime = await ensureCppRuntime();
  const t0 = performance.now();
  const result = await runtime.compile({
    source: String(code || ""),
    fileName: "main.cpp",
    flags: ["-O2", "-std=c++14", "-fno-exceptions"],
  });
  const elapsedMs = performance.now() - t0;

  if (!result.module) {
    return {
      success: false,
      compile_output: String(result.compileOutput || "Compilation failed"),
      elapsed_ms: elapsedMs,
    };
  }

  const programId = cppProgramIdCounter++;
  cppPrograms.set(programId, result.module);
  return {
    success: true,
    program_id: programId,
    compile_output: String(result.compileOutput || ""),
    elapsed_ms: elapsedMs,
  };
}

function createCollector() {
  const decoder = new TextDecoder();
  let text = "";
  return {
    push(chunk) {
      text += decoder.decode(chunk, { stream: true });
    },
    finish() {
      text += decoder.decode();
      return text;
    },
  };
}

async function runCpp(programId, inputData) {
  const runtime = await ensureCppRuntime();
  const module = cppPrograms.get(Number(programId));
  if (!module) {
    throw new Error("C++ compiled module not found");
  }

  const encoder = new TextEncoder();
  const stdoutCollector = createCollector();
  const stderrCollector = createCollector();

  const fds = [
    new runtime.OpenFile(new runtime.File(encoder.encode(String(inputData || "")))),
    new runtime.ConsoleStdout((chunk) => stdoutCollector.push(chunk)),
    new runtime.ConsoleStdout((chunk) => stderrCollector.push(chunk)),
  ];

  const wasi = new runtime.WASI([], [], fds);
  const t0 = performance.now();
  const instance = await WebAssembly.instantiate(module, {
    wasi_snapshot_preview1: wasi.wasiImport,
    wasi_unstable: wasi.wasiImport,
  });
  const exitCode = Number(wasi.start(instance));
  const elapsedMs = performance.now() - t0;

  return {
    stdout: stdoutCollector.finish(),
    stderr: stderrCollector.finish(),
    exit_code: exitCode,
    error: "",
    elapsed_ms: elapsedMs,
  };
}

function dropCppProgram(programId) {
  cppPrograms.delete(Number(programId));
}

self.onmessage = async (event) => {
  const message = event.data || {};
  const id = message.id;
  const action = message.action;

  if (typeof id !== "number") {
    return;
  }

  try {
    if (action === "init") {
      await ensurePyodide();
      self.postMessage({ id, ok: true, payload: { ready: true } });
      return;
    }

    if (action === "initCpp") {
      await ensureCppRuntime();
      self.postMessage({ id, ok: true, payload: { ready: true } });
      return;
    }

    if (action === "runPython") {
      const payload = message.payload || {};
      const t0 = performance.now();
      const result = await runPython(String(payload.code || ""), String(payload.input || ""));
      const elapsedMs = performance.now() - t0;
      self.postMessage({
        id,
        ok: true,
        payload: {
          ...result,
          elapsed_ms: elapsedMs,
        },
      });
      return;
    }

    if (action === "compileCpp") {
      const payload = message.payload || {};
      const result = await compileCpp(String(payload.code || ""));
      self.postMessage({ id, ok: true, payload: result });
      return;
    }

    if (action === "runCpp") {
      const payload = message.payload || {};
      const result = await runCpp(payload.program_id, String(payload.input || ""));
      self.postMessage({ id, ok: true, payload: result });
      return;
    }

    if (action === "dropCppProgram") {
      const payload = message.payload || {};
      dropCppProgram(payload.program_id);
      self.postMessage({ id, ok: true, payload: { dropped: true } });
      return;
    }

    throw new Error(`Unsupported action: ${String(action)}`);
  } catch (error) {
    self.postMessage({
      id,
      ok: false,
      error: error && error.message ? error.message : String(error),
    });
  }
};
