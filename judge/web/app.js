const dataApi = {
  async getManifest() {
    const res = await fetch("/problems_manifest.json", { cache: "no-store" });
    return handleJsonResponse(res);
  },
  async getTestcase(pid, testcaseName, ext) {
    const safePid = encodeURIComponent(pid);
    const safeCase = encodeURIComponent(testcaseName);
    const res = await fetch(`/problems/${safePid}/testcases/${safeCase}.${ext}`, {
      cache: "no-store",
    });
    return handleTextResponse(res);
  },
};

async function handleJsonResponse(res) {
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(data?.message || `HTTP ${res.status}`);
  }
  return data;
}

async function handleTextResponse(res) {
  const data = await res.text().catch(() => "");
  if (!res.ok) {
    throw new Error(`HTTP ${res.status}`);
  }
  return data;
}

const verdictLabels = {
  AC: "Accepted",
  WA: "Wrong Answer",
  TLE: "Time Limit Exceeded",
  RE: "Runtime Error",
  CE: "Compilation Error",
  SE: "System Error",
};

const state = {
  problems: [],
  problemByPid: new Map(),
  selectedPid: null,
  selectedProblem: null,
  currentLanguage: null,
  editor: null,
  autosaveTimer: null,
};

const testcaseCache = new Map();

const STORAGE_PREFIX = "gpe-judge-draft-v2";

const els = {
  serverStatus: document.querySelector("#serverStatus"),
  problemSidebar: document.querySelector("#problemSidebar"),
  toggleProblemPanelBtn: document.querySelector("#toggleProblemPanelBtn"),
  problemSearch: document.querySelector("#problemSearch"),
  problemList: document.querySelector("#problemList"),
  selectedProblemTitle: document.querySelector("#selectedProblemTitle"),
  selectedProblemMeta: document.querySelector("#selectedProblemMeta"),
  problemLink: document.querySelector("#problemLink"),
  problemDescription: document.querySelector("#problemDescription"),
  sampleList: document.querySelector("#sampleList"),
  languageSelect: document.querySelector("#languageSelect"),
  codeEditor: document.querySelector("#codeEditor"),
  runBtn: document.querySelector("#runBtn"),
  resetBtn: document.querySelector("#resetBtn"),
  draftStatus: document.querySelector("#draftStatus"),
  summaryBadge: document.querySelector("#summaryBadge"),
  resultBody: document.querySelector("#resultBody"),
  problemItemTpl: document.querySelector("#problemItemTpl"),
  sampleItemTpl: document.querySelector("#sampleItemTpl"),
  sampleModal: document.querySelector("#sampleModal"),
  sampleModalBackdrop: document.querySelector("#sampleModalBackdrop"),
  sampleModalCloseBtn: document.querySelector("#sampleModalCloseBtn"),
  sampleModalTitle: document.querySelector("#sampleModalTitle"),
  sampleModalInput: document.querySelector("#sampleModalInput"),
  sampleModalOutput: document.querySelector("#sampleModalOutput"),
};

const starterCode = {
  cpp14: `#include <iostream>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // Write your C++14 solution here.

    return 0;
}
`,
  python39: `# Write your Python 3.9 solution here
import sys

def main():
    pass

if __name__ == "__main__":
    main()
`,
};

function editorModeByLanguage(lang) {
  return lang === "cpp14" ? "text/x-c++src" : "python";
}

function setSummary(text, cls = "neutral") {
  els.summaryBadge.textContent = text;
  els.summaryBadge.className = `summary ${cls}`;
}

function setServerStatus(text, ok = false) {
  els.serverStatus.textContent = text;
  els.serverStatus.style.borderColor = ok ? "rgba(29,127,78,0.45)" : "rgba(187,62,62,0.45)";
  els.serverStatus.style.color = ok ? "#1d7f4e" : "#bb3e3e";
}

function verdictClass(verdict) {
  const lower = String(verdict || "").toLowerCase();
  return `v-${lower}`;
}

function summaryClass(verdict) {
  const lower = String(verdict || "").toLowerCase();
  if (["ac", "wa", "tle", "re", "ce", "se"].includes(lower)) return lower;
  return "neutral";
}

function setDraftStatus(text) {
  els.draftStatus.textContent = text;
}

function draftKey(pid, lang) {
  const problemPart = pid || "global";
  return `${STORAGE_PREFIX}:${problemPart}:${lang}`;
}

function getActiveLanguage() {
  return state.currentLanguage || els.languageSelect.value;
}

function getEditorValue() {
  return state.editor ? state.editor.getValue() : "";
}

function setEditorValue(value) {
  if (state.editor) {
    state.editor.setValue(value);
    state.editor.focus();
  }
}

function saveDraftForLanguage(lang) {
  const pid = state.selectedPid || "global";
  const code = getEditorValue();
  localStorage.setItem(draftKey(pid, lang), code);
  setDraftStatus(`已自動儲存 ${new Date().toLocaleTimeString()}`);
}

function saveDraftNow() {
  saveDraftForLanguage(getActiveLanguage());
}

function scheduleAutosave() {
  if (state.autosaveTimer) {
    window.clearTimeout(state.autosaveTimer);
  }
  setDraftStatus("草稿儲存中...");
  state.autosaveTimer = window.setTimeout(() => {
    saveDraftNow();
    state.autosaveTimer = null;
  }, 450);
}

function loadDraftOrStarter(pid, lang) {
  const saved = localStorage.getItem(draftKey(pid || "global", lang));
  if (saved !== null && saved !== undefined) {
    const savedText = String(saved);
    if (savedText.trim()) {
      return savedText;
    }
  }
  return starterCode[lang] || "";
}

function resetToTemplate() {
  const lang = getActiveLanguage();
  const pid = state.selectedPid || "global";
  const template = starterCode[lang] || "";
  setEditorValue(template);
  localStorage.setItem(draftKey(pid, lang), template);
  setDraftStatus("已重置為範本");
}

function setEditorLanguage(lang) {
  if (!state.editor) return;
  state.editor.setOption("mode", editorModeByLanguage(lang));
}

function renderProblemList(items) {
  els.problemList.innerHTML = "";
  for (const p of items) {
    const node = els.problemItemTpl.content.firstElementChild.cloneNode(true);
    node.dataset.pid = p.pid;
    node.querySelector(".pid").textContent = p.pid;
    node.querySelector(".name").textContent = p.name;
    node.querySelector(".tests").textContent = `${p.testcase_count ?? 0} tests`;
    if (p.pid === state.selectedPid) node.classList.add("active");
    node.addEventListener("click", () => selectProblem(p.pid));
    els.problemList.appendChild(node);
  }
}

function applySearch() {
  const q = els.problemSearch.value.trim().toLowerCase();
  const filtered = q
    ? state.problems.filter(
        (p) => p.pid.toLowerCase().includes(q) || p.name.toLowerCase().includes(q)
      )
    : state.problems;
  renderProblemList(filtered);
}

function renderProblemHeader() {
  if (!state.selectedProblem) {
    els.selectedProblemTitle.textContent = "請選擇題目";
    els.selectedProblemMeta.textContent = "-";
    els.problemDescription.textContent = "請先選擇題目。";
    els.problemDescription.hidden = false;
    els.problemLink.disabled = true;
    els.sampleList.innerHTML = "";
    return;
  }

  const p = state.selectedProblem;
  const categories = Array.isArray(p.category) && p.category.length ? p.category.join(", ") : "無";
  els.selectedProblemTitle.textContent = `${p.pid} · ${p.name}`;
  els.selectedProblemMeta.textContent = `TL: ${p.time_limit}s · 類別: ${categories} · 測資: ${p.testcase_count}`;
  const description = typeof p.description === "string" ? p.description.trim() : "";
  els.problemDescription.textContent = description || "此題尚未提供本地敘述，請使用「查看原題」。";
  els.problemDescription.hidden = false;
  els.problemLink.disabled = !p.problem_url;

  const sampleNames = Array.isArray(p.testcase_names) ? p.testcase_names.slice(0, 2) : [];
  renderSamples(sampleNames);
}

async function fetchTestcasePair(pid, testcaseName) {
  const key = `${pid}:${testcaseName}`;
  if (testcaseCache.has(key)) {
    return testcaseCache.get(key);
  }
  const pair = await Promise.all([
    dataApi.getTestcase(pid, testcaseName, "in"),
    dataApi.getTestcase(pid, testcaseName, "out"),
  ]).then(([input, output]) => ({ input, output }));
  testcaseCache.set(key, pair);
  return pair;
}

async function openSampleModalByName(testcaseName) {
  if (!els.sampleModal || !state.selectedPid) return;
  els.sampleModalTitle.textContent = `範例測資 ${testcaseName}`;
  els.sampleModalInput.textContent = "載入中...";
  els.sampleModalOutput.textContent = "載入中...";
  els.sampleModal.classList.add("open");
  els.sampleModal.setAttribute("aria-hidden", "false");
  document.body.classList.add("modal-open");

  try {
    const pair = await fetchTestcasePair(state.selectedPid, testcaseName);
    els.sampleModalInput.textContent = truncateText(pair.input, 1200);
    els.sampleModalOutput.textContent = truncateText(pair.output, 1200);
  } catch (error) {
    const message = `載入失敗：${error.message}`;
    els.sampleModalInput.textContent = message;
    els.sampleModalOutput.textContent = message;
  }
}

function closeSampleModal() {
  if (!els.sampleModal) return;
  els.sampleModal.classList.remove("open");
  els.sampleModal.setAttribute("aria-hidden", "true");
  document.body.classList.remove("modal-open");
}

function renderSamples(sampleNames) {
  els.sampleList.innerHTML = "";
  if (!sampleNames.length) {
    const empty = document.createElement("p");
    empty.className = "placeholder";
    empty.textContent = "目前沒有範例測資。";
    els.sampleList.appendChild(empty);
    return;
  }

  for (const testcaseName of sampleNames) {
    const node = els.sampleItemTpl.content.firstElementChild.cloneNode(true);
    node.querySelector(".sample-trigger-name").textContent = `範例測資 ${testcaseName}`;
    node.addEventListener("click", () => openSampleModalByName(testcaseName));
    els.sampleList.appendChild(node);
  }
}

function renderResult(result) {
  els.resultBody.innerHTML = "";
  setSummary(
    `${result.overall_verdict} · ${result.passed}/${result.total}`,
    summaryClass(result.overall_verdict)
  );

  for (const r of result.results || []) {
    const card = document.createElement("article");
    card.className = "case";
    const top = document.createElement("div");
    top.className = "case-top";
    top.innerHTML = `
      <strong>Test ${escapeHtml(r.testcase || "-")}</strong>
      <span class="${verdictClass(r.verdict)}">${escapeHtml(r.verdict)} · ${Math.round(
      Number(r.time_ms || 0)
    )}ms</span>
    `;
    card.appendChild(top);

    if (r.verdict === "WA") {
      const pre = document.createElement("pre");
      pre.textContent = `Expected:\n${r.expected || ""}\n\nActual:\n${r.actual || ""}`;
      card.appendChild(pre);
    } else if (r.error_msg) {
      const pre = document.createElement("pre");
      pre.textContent = r.error_msg;
      card.appendChild(pre);
    }
    els.resultBody.appendChild(card);
  }
}

function showMessage(msg) {
  els.resultBody.innerHTML = `<p class="placeholder">${escapeHtml(msg)}</p>`;
}

function escapeHtml(text) {
  return String(text)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function truncateText(text, limit = 900) {
  const normalized = String(text || "").replace(/\r\n/g, "\n").replace(/\r/g, "\n").replace(/\n+$/, "");
  if (normalized.length <= limit) {
    return normalized;
  }
  return `${normalized.slice(0, limit)}\n... (truncated)`;
}

async function selectProblem(pid) {
  try {
    saveDraftNow();
    closeSampleModal();

    state.selectedPid = pid;
    state.selectedProblem = state.problemByPid.get(pid) || null;

    applySearch();
    renderProblemHeader();

    const lang = els.languageSelect.value;
    const draft = loadDraftOrStarter(pid, lang);
    setEditorValue(draft);
    setDraftStatus("已載入草稿");

    if (window.matchMedia("(max-width: 1100px)").matches) {
      els.problemSidebar.classList.remove("open");
    }
  } catch (error) {
    showMessage(`讀取題目失敗：${error.message}`);
  }
}

function initEditor() {
  state.editor = CodeMirror.fromTextArea(els.codeEditor, {
    mode: editorModeByLanguage(els.languageSelect.value),
    lineNumbers: true,
    lineWrapping: false,
    indentUnit: 4,
    tabSize: 4,
    indentWithTabs: false,
    smartIndent: true,
    matchBrackets: true,
    autoCloseBrackets: true,
    extraKeys: {
      Tab(cm) {
        if (cm.somethingSelected()) {
          cm.indentSelection("add");
        } else {
          cm.replaceSelection("    ", "end", "+input");
        }
      },
      "Shift-Tab"(cm) {
        cm.indentSelection("subtract");
      },
      Enter(cm) {
        cm.execCommand("newlineAndIndent");
      },
    },
  });

  state.editor.on("change", () => {
    scheduleAutosave();
  });
}

function normalizeOutput(text) {
  const normalized = String(text || "").replace(/\r\n/g, "\n").replace(/\r/g, "\n");
  const trimmed = normalized.replace(/\n+$/, "");
  const lines = trimmed.split("\n");
  return lines.map((line) => line.replace(/[ \t]+$/g, "")).join("\n");
}

function compareOutputs(expected, actual) {
  return normalizeOutput(expected) === normalizeOutput(actual);
}

function firstNonAC(results) {
  for (const item of results) {
    if (item.verdict !== "AC") {
      return item.verdict;
    }
  }
  return results.length ? "AC" : "SE";
}

function createJudgeRuntime() {
  let worker = null;
  let nextId = 1;
  const pending = new Map();
  let pythonReady = false;
  let cppReady = false;

  function ensureWorker() {
    if (worker) {
      return worker;
    }
    worker = new Worker("./judge-worker.js");
    worker.addEventListener("message", (event) => {
      const message = event.data || {};
      const pendingItem = pending.get(message.id);
      if (!pendingItem) return;
      pending.delete(message.id);
      window.clearTimeout(pendingItem.timer);
      if (message.ok) {
        pendingItem.resolve(message.payload);
      } else {
        pendingItem.reject(new Error(message.error || "Worker error"));
      }
    });
    worker.addEventListener("error", (event) => {
      const reason = event.message || "Worker failed";
      for (const item of pending.values()) {
        window.clearTimeout(item.timer);
        item.reject(new Error(reason));
      }
      pending.clear();
      worker = null;
      pythonReady = false;
      cppReady = false;
    });
    return worker;
  }

  function terminateWorker() {
    if (!worker) return;
    worker.terminate();
    worker = null;
    for (const item of pending.values()) {
      window.clearTimeout(item.timer);
      item.reject(new Error("Worker terminated"));
    }
    pending.clear();
    pythonReady = false;
    cppReady = false;
  }

  function callWorker(action, payload, timeoutMs) {
    const activeWorker = ensureWorker();
    const id = nextId++;
    return new Promise((resolve, reject) => {
      const timer = window.setTimeout(() => {
        pending.delete(id);
        reject(new Error("Worker timeout"));
      }, timeoutMs);
      pending.set(id, { resolve, reject, timer });
      activeWorker.postMessage({ id, action, payload });
    });
  }

  function isLanguageReady(language) {
    if (language === "cpp14") return cppReady;
    if (language === "python39") return pythonReady;
    return false;
  }

  async function ensureLanguageReady(language) {
    if (language === "python39") {
      if (!pythonReady) {
        await callWorker("init", {}, 90_000);
        pythonReady = true;
      }
      return;
    }

    if (language === "cpp14") {
      if (!cppReady) {
        await callWorker("initCpp", {}, 120_000);
        cppReady = true;
      }
      return;
    }

    throw new Error("Unsupported language runtime");
  }

  async function runPythonCase(code, input, timeLimitSec) {
    const timeLimitMs = Math.max(100, Math.floor(Number(timeLimitSec || 3) * 1000));
    const timeoutMs = timeLimitMs + 200;
    try {
      const output = await callWorker(
        "runPython",
        {
          code,
          input,
        },
        timeoutMs
      );
      return {
        stdout: String(output.stdout || ""),
        stderr: String(output.stderr || ""),
        exit_code: Number(output.exit_code || 0),
        error: String(output.error || ""),
        elapsed_ms: Number(output.elapsed_ms || 0),
        timed_out: false,
      };
    } catch (error) {
      if (String(error.message || "").includes("timeout")) {
        terminateWorker();
        return {
          stdout: "",
          stderr: "",
          exit_code: 1,
          error: "TLE",
          elapsed_ms: timeLimitMs,
          timed_out: true,
        };
      }
      throw error;
    }
  }

  async function compileCpp(code) {
    try {
      return await callWorker(
        "compileCpp",
        {
          code,
        },
        240_000
      );
    } catch (error) {
      if (String(error.message || "").includes("timeout")) {
        terminateWorker();
      }
      throw error;
    }
  }

  async function runCppCase(programId, input, timeLimitSec) {
    const timeLimitMs = Math.max(100, Math.floor(Number(timeLimitSec || 3) * 1000));
    const timeoutMs = timeLimitMs + 250;
    try {
      const output = await callWorker(
        "runCpp",
        {
          program_id: programId,
          input,
        },
        timeoutMs
      );
      return {
        stdout: String(output.stdout || ""),
        stderr: String(output.stderr || ""),
        exit_code: Number(output.exit_code || 0),
        error: String(output.error || ""),
        elapsed_ms: Number(output.elapsed_ms || 0),
        timed_out: false,
      };
    } catch (error) {
      if (String(error.message || "").includes("timeout")) {
        terminateWorker();
        return {
          stdout: "",
          stderr: "",
          exit_code: 1,
          error: "TLE",
          elapsed_ms: timeLimitMs,
          timed_out: true,
        };
      }
      throw error;
    }
  }

  async function dropCppProgram(programId) {
    if (!programId) return;
    try {
      await callWorker(
        "dropCppProgram",
        {
          program_id: programId,
        },
        3_000
      );
    } catch (error) {
      // Ignore cleanup errors.
    }
  }

  return { isLanguageReady, ensureLanguageReady, runPythonCase, compileCpp, runCppCase, dropCppProgram };
}

const judgeRuntime = createJudgeRuntime();

async function judgeSubmission(problem, language, code) {
  if (!problem) {
    throw new Error("Problem not selected");
  }

  const testcaseNames = Array.isArray(problem.testcase_names) ? problem.testcase_names : [];
  if (!testcaseNames.length) {
    return {
      problem_id: problem.pid,
      language,
      language_label: language === "cpp14" ? "C++14" : "Python 3.9",
      overall_verdict: "SE",
      overall_label: verdictLabels.SE,
      passed: 0,
      total: 1,
      results: [
        {
          testcase: "-",
          verdict: "SE",
          label: verdictLabels.SE,
          time_ms: 0,
          expected: "",
          actual: "",
          error_msg: "No testcases found for this problem.",
        },
      ],
    };
  }

  let passed = 0;
  const tl = Number(problem.time_limit || 3);
  const results = [];
  if (language === "python39") {
    for (const testcaseName of testcaseNames) {
      const pair = await fetchTestcasePair(problem.pid, testcaseName);
      const execResult = await judgeRuntime.runPythonCase(code, pair.input, tl);

      if (execResult.timed_out) {
        results.push({
          testcase: testcaseName,
          verdict: "TLE",
          label: verdictLabels.TLE,
          time_ms: execResult.elapsed_ms,
          expected: "",
          actual: "",
          error_msg: "",
        });
        continue;
      }

      if (execResult.error || execResult.exit_code !== 0) {
        const detail = execResult.error || execResult.stderr || `Runtime Error (exit ${execResult.exit_code})`;
        results.push({
          testcase: testcaseName,
          verdict: "RE",
          label: verdictLabels.RE,
          time_ms: execResult.elapsed_ms,
          expected: "",
          actual: "",
          error_msg: detail.slice(0, 1200),
        });
        continue;
      }

      if (compareOutputs(pair.output, execResult.stdout)) {
        passed += 1;
        results.push({
          testcase: testcaseName,
          verdict: "AC",
          label: verdictLabels.AC,
          time_ms: execResult.elapsed_ms,
          expected: "",
          actual: "",
          error_msg: "",
        });
        continue;
      }

      results.push({
        testcase: testcaseName,
        verdict: "WA",
        label: verdictLabels.WA,
        time_ms: execResult.elapsed_ms,
        expected: pair.output.slice(0, 200),
        actual: execResult.stdout.slice(0, 200),
        error_msg: "",
      });
    }
  } else if (language === "cpp14") {
    const compileResult = await judgeRuntime.compileCpp(code);
    if (!compileResult.success) {
      return {
        problem_id: problem.pid,
        language,
        language_label: "C++14",
        overall_verdict: "CE",
        overall_label: verdictLabels.CE,
        passed: 0,
        total: 1,
        results: [
          {
            testcase: "",
            verdict: "CE",
            label: verdictLabels.CE,
            time_ms: Number(compileResult.elapsed_ms || 0),
            expected: "",
            actual: "",
            error_msg: String(compileResult.compile_output || "Compilation Error").slice(0, 2000),
          },
        ],
      };
    }

    const programId = compileResult.program_id;
    try {
      for (let i = 0; i < testcaseNames.length; i += 1) {
        const testcaseName = testcaseNames[i];
        const pair = await fetchTestcasePair(problem.pid, testcaseName);
        const execResult = await judgeRuntime.runCppCase(programId, pair.input, tl);

        if (execResult.timed_out) {
          results.push({
            testcase: testcaseName,
            verdict: "TLE",
            label: verdictLabels.TLE,
            time_ms: execResult.elapsed_ms,
            expected: "",
            actual: "",
            error_msg: "",
          });
          for (let j = i + 1; j < testcaseNames.length; j += 1) {
            results.push({
              testcase: testcaseNames[j],
              verdict: "TLE",
              label: verdictLabels.TLE,
              time_ms: 0,
              expected: "",
              actual: "",
              error_msg: "Skipped after timeout.",
            });
          }
          break;
        }

        if (execResult.error || execResult.exit_code !== 0) {
          const detail = execResult.error || execResult.stderr || `Runtime Error (exit ${execResult.exit_code})`;
          results.push({
            testcase: testcaseName,
            verdict: "RE",
            label: verdictLabels.RE,
            time_ms: execResult.elapsed_ms,
            expected: "",
            actual: "",
            error_msg: detail.slice(0, 1200),
          });
          continue;
        }

        if (compareOutputs(pair.output, execResult.stdout)) {
          passed += 1;
          results.push({
            testcase: testcaseName,
            verdict: "AC",
            label: verdictLabels.AC,
            time_ms: execResult.elapsed_ms,
            expected: "",
            actual: "",
            error_msg: "",
          });
          continue;
        }

        results.push({
          testcase: testcaseName,
          verdict: "WA",
          label: verdictLabels.WA,
          time_ms: execResult.elapsed_ms,
          expected: pair.output.slice(0, 200),
          actual: execResult.stdout.slice(0, 200),
          error_msg: "",
        });
      }
    } finally {
      await judgeRuntime.dropCppProgram(programId);
    }
  } else {
    return {
      problem_id: problem.pid,
      language,
      language_label: "Unknown",
      overall_verdict: "SE",
      overall_label: verdictLabels.SE,
      passed: 0,
      total: 1,
      results: [
        {
          testcase: "-",
          verdict: "SE",
          label: verdictLabels.SE,
          time_ms: 0,
          expected: "",
          actual: "",
          error_msg: "Unsupported language.",
        },
      ],
    };
  }

  const overallVerdict = firstNonAC(results);
  return {
    problem_id: problem.pid,
    language,
    language_label: language === "cpp14" ? "C++14" : "Python 3.9",
    overall_verdict: overallVerdict,
    overall_label: verdictLabels[overallVerdict] || verdictLabels.SE,
    passed,
    total: results.length,
    results,
  };
}

async function handleRun() {
  if (!state.selectedPid || !state.selectedProblem) {
    showMessage("請先選擇題目。");
    return;
  }

  const code = getEditorValue();
  if (!code.trim()) {
    showMessage("請輸入程式碼。");
    return;
  }

  const language = els.languageSelect.value;
  saveDraftNow();
  els.runBtn.disabled = true;
  setSummary("批改中...", "neutral");
  showMessage("瀏覽器本地批改中，請稍候...");

  try {
    if (!judgeRuntime.isLanguageReady(language)) {
      if (language === "cpp14") {
        showMessage("正在載入 C++ Runtime（首次可能較久，完成後會開始編譯）...");
      } else {
        showMessage("正在載入 Python Runtime（首次需要下載）...");
      }
    }
    await judgeRuntime.ensureLanguageReady(language);

    if (language === "cpp14") {
      showMessage("C++ WASM 編譯與批改中，請稍候...");
    } else {
      showMessage("Python WASM 批改中，請稍候...");
    }

    const result = await judgeSubmission(state.selectedProblem, language, code);
    renderResult(result);
  } catch (error) {
    setSummary("提交失敗", "se");
    showMessage(`批改失敗：${error.message}`);
  } finally {
    els.runBtn.disabled = false;
  }
}

function onLanguageChange() {
  const nextLang = els.languageSelect.value;
  const previousLang = state.currentLanguage;

  if (previousLang && previousLang !== nextLang) {
    saveDraftForLanguage(previousLang);
  }

  state.currentLanguage = nextLang;
  setEditorLanguage(nextLang);
  const draft = loadDraftOrStarter(state.selectedPid, nextLang);
  setEditorValue(draft);
  const starter = starterCode[nextLang] || "";
  setDraftStatus(draft === starter ? "已切換語言並載入範本" : "已切換語言並載入草稿");
}

function openProblemLink() {
  const url = state.selectedProblem?.problem_url;
  if (!url) return;
  window.open(url, "_blank", "noopener");
}

async function boot() {
  initEditor();
  state.currentLanguage = els.languageSelect.value;
  setServerStatus("載入本地題庫中...", true);

  try {
    const manifest = await dataApi.getManifest();
    const problems = Array.isArray(manifest.problems) ? manifest.problems : [];
    state.problems = problems.sort((a, b) => String(a.pid).localeCompare(String(b.pid)));
    state.problemByPid = new Map(state.problems.map((p) => [p.pid, p]));

    renderProblemList(state.problems);
    if (state.problems.length > 0) {
      await selectProblem(state.problems[0].pid);
    } else {
      setEditorValue(loadDraftOrStarter(null, els.languageSelect.value));
      setDraftStatus("已載入範本");
      showMessage("沒有可用題目。");
    }
  } catch (error) {
    setServerStatus(`載入失敗 · ${error.message}`, false);
    showMessage("無法讀取 problems_manifest.json，請先執行 build_frontend_manifest.py。");
    return;
  }

  setServerStatus("純前端模式 · Runtime 按需載入", true);
}

els.problemSearch.addEventListener("input", applySearch);
els.languageSelect.addEventListener("change", onLanguageChange);
els.runBtn.addEventListener("click", handleRun);
els.resetBtn.addEventListener("click", resetToTemplate);
els.problemLink.addEventListener("click", openProblemLink);
els.toggleProblemPanelBtn.addEventListener("click", () => {
  els.problemSidebar.classList.toggle("open");
});
if (els.sampleModalCloseBtn) {
  els.sampleModalCloseBtn.addEventListener("click", closeSampleModal);
}
if (els.sampleModalBackdrop) {
  els.sampleModalBackdrop.addEventListener("click", closeSampleModal);
}
window.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && els.sampleModal?.classList.contains("open")) {
    closeSampleModal();
  }
});
window.addEventListener("beforeunload", () => {
  try {
    saveDraftNow();
  } catch (error) {
    // Ignore unload-time localStorage edge cases.
  }
});

boot();
