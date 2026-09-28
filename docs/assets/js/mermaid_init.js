document.addEventListener("DOMContentLoaded", async function () {
  if (typeof mermaid === "undefined") return;

  mermaid.initialize({
    startOnLoad: false,
    theme: "base",
    themeVariables: {
      fontFamily: "Inter, -apple-system, BlinkMacSystemFont, sans-serif",
      fontSize: "13px",
      primaryColor: "#ffffff",
      primaryBorderColor: "#0284c7",
      primaryTextColor: "#07090e",
      secondaryColor: "#fafafa",
      secondaryBorderColor: "#cbd5e1",
      secondaryTextColor: "#334155",
      tertiaryColor: "#f8fafc",
      tertiaryBorderColor: "#e2e8f0",
      tertiaryTextColor: "#475569",
      lineColor: "#0284c7",
      textColor: "#07090e",
      mainBkg: "#ffffff",
      nodeBorder: "#0284c7",
      clusterBkg: "#f8fafc",
      clusterBorder: "#cbd5e1",
      edgeLabelBackground: "#ffffff",
      arrowheadColor: "#0284c7"
    },
    flowchart: {
      htmlLabels: false,
      curve: "linear",
      padding: 24,
      nodeSpacing: 50,
      rankSpacing: 50
    }
  });

  const mermaidBlocks = Array.from(document.querySelectorAll("pre.mermaid, .mermaid"));
  for (let i = 0; i < mermaidBlocks.length; i++) {
    const el = mermaidBlocks[i];
    const codeEl = el.querySelector("code");
    const rawText = (codeEl ? codeEl.textContent : el.textContent).trim();
    if (!rawText) continue;

    const id = "mermaid-diagram-" + i;
    try {
      const { svg } = await mermaid.render(id, rawText);
      const wrapper = document.createElement("div");
      wrapper.className = "mermaid-container";
      wrapper.style.textAlign = "center";
      wrapper.style.margin = "2rem 0";
      wrapper.style.overflowX = "auto";
      wrapper.innerHTML = svg;
      el.parentNode.replaceChild(wrapper, el);
    } catch (err) {
      console.error("Erro ao renderizar diagrama mermaid:", err);
    }
  }
});