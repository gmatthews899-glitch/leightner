const table = document.querySelector("[data-orders-table]");

if (table) {
  const headers = Array.from(table.querySelectorAll("thead th[data-column]"));
  const tbody = table.querySelector("tbody");
  const numericColumns = new Set(["ship_qty", "backorder_qty", "total_qty"]);
  const dateColumns = new Set(["estimated_ship_date"]);
  let activeColumn = "";
  let activeDirection = "asc";

  // Read raw sort values so formatted cells like dates and pills still sort predictably.
  const getCellValue = (row, index) => {
    const cell = row.children[index];
    return cell?.dataset.value ?? cell?.textContent?.trim() ?? "";
  };

  const compareValues = (left, right, column, direction) => {
    if (dateColumns.has(column)) {
      const leftEmpty = left === "";
      const rightEmpty = right === "";

      if (leftEmpty && rightEmpty) {
        return 0;
      }
      if (leftEmpty) {
        return 1;
      }
      if (rightEmpty) {
        return -1;
      }

      return (new Date(left).getTime() - new Date(right).getTime()) * direction;
    }

    if (numericColumns.has(column)) {
      return (Number(left) - Number(right)) * direction;
    }

    return left.localeCompare(right, undefined, { sensitivity: "base" }) * direction;
  };

  headers.forEach((header, index) => {
    header.addEventListener("click", () => {
      const column = header.dataset.column ?? "";
      activeDirection = activeColumn === column && activeDirection === "asc" ? "desc" : "asc";
      activeColumn = column;

      headers.forEach((item) => {
        delete item.dataset.sort;
      });
      header.dataset.sort = activeDirection;

      const direction = activeDirection === "asc" ? 1 : -1;
      const rows = Array.from(tbody.querySelectorAll("tr"));

      rows.sort((leftRow, rightRow) => {
        const leftValue = getCellValue(leftRow, index);
        const rightValue = getCellValue(rightRow, index);
        return compareValues(leftValue, rightValue, column, direction);
      });

      rows.forEach((row) => {
        tbody.appendChild(row);
      });
    });
  });
}
