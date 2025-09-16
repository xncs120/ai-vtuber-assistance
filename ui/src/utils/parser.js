export const extractJSONObjects = (str) => {
  const objects = [];
  const lines = str.split(/\r?\n/);
  let remainingLines = [];

  for (const line of lines) {
    if (line.startsWith("data:")) {
      const jsonStr = line.slice(5).trim();
      try {
        const json = JSON.parse(jsonStr);
        objects.push(json);
      } catch (err) {
        remainingLines.push(line);
      }
    } else {
      remainingLines.push(line);
    }
  }

  const remaining = remainingLines.join("\n");
  return { objects, remaining };
};