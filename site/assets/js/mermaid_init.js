document.addEventListener("DOMContentLoaded", function () {
  if (typeof mermaid !== "undefined") {
    mermaid.initialize({
      startOnLoad: true,
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
        htmlLabels: true,
        curve: "linear",
        padding: 12
      }
    });
  }
});
