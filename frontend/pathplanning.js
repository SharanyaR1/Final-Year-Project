function loadAdjacencyMatrix() {
  fetch("/get_adjacency_matrix") // Fetch from the new API route
    .then(function (response) {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error("Failed to fetch the adjacency matrix.");
      }
    })
    .then(function (data) {
      var adjacencyMatrixContainer = document.getElementById(
        "adjacencyMatrixContainer"
      );
      if (!adjacencyMatrixContainer) {
        throw new Error("adjacencyMatrixContainer not found.");
      }

      adjacencyMatrixContainer.innerHTML = "";

      if (!data || !Array.isArray(data)) {
        throw new Error("Adjacency matrix data is missing or invalid.");
      }

      // Create grid
      var matrixGrid = document.createElement("div");
      matrixGrid.classList.add("matrix-grid");

      // Populate grid with matrix data
      data.forEach(function (row) {
        row.forEach(function (distance) {
          var cellElement = document.createElement("div");
          cellElement.classList.add("matrix-cell");
          cellElement.textContent = distance;
          matrixGrid.appendChild(cellElement);
        });
      });

      // Append matrix grid to container
      adjacencyMatrixContainer.appendChild(matrixGrid);
    })
    .catch(function (error) {
      console.error("An error occurred: ", error);
      alert("An error occurred: " + error.message);
    });
}

// fetch("/add_random_dustbins", {
//   method: "POST",
//   headers: {
//     "Content-Type": "application/json",
//   },
//   body: JSON.stringify({ numDustbins: 10 }),
// })
//   .then((response) => response.json())
//   .then((data) => {
//     if (data.message === "Dustbins added successfully") {
//       const dustbins = data.dustbins;
//       dustbins.forEach((dustbin) => {
//         // Assuming you have a function to display a dustbin on the map
//         displayDustbinOnMap(dustbin.id, dustbin.latitude, dustbin.longitude);
//       });
//     } else {
//       console.error(data.message);
//     }
//   })
//   .catch((error) => console.error("Error:", error));

function performPathPlanning() {
  window.location.href = "pathplanning.html";
}
