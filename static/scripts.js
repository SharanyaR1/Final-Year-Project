document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("dustbinForm")
    .addEventListener("submit", function (event) {
      event.preventDefault();
      submitDustbin();
    });

  document
    .getElementById("randomDustbinForm")
    .addEventListener("submit", function (event) {
      event.preventDefault();
      submitRandomDustbins();
    });

  document
    .getElementById("calculateRouteButton")
    .addEventListener("click", function () {
      calculateOptimizedRoute();
    });

  document
    .getElementById("clearAllDustbinsButton")
    .addEventListener("click", function () {
      clearAllDustbins();
    });

  loadDustbins();
});

const depotIconPath = "../assets/home.png";

function submitDustbin() {
  var latitude = document.getElementById("latitude").value;
  var longitude = document.getElementById("longitude").value;
  var capacity = document.getElementById("capacity").value;

  if (!latitude || !longitude || !capacity) {
    alert("Please fill in all fields.");
    return;
  }

  var data = {
    latitude: latitude,
    longitude: longitude,
    capacity: capacity,
  };

  fetch("/create_dustbin", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then(function (response) {
      if (response.status === 201) {
        alert("Dustbin created successfully!");
        clearFields();
        loadDustbins();
      } else {
        alert("Failed to create dustbin.");
      }
    })
    .catch(function (error) {
      alert("An error occurred: " + error);
    });
}

function submitRandomDustbins() {
  var numDustbins = document.getElementById("numDustbins").value;

  if (!numDustbins) {
    alert("Please enter the number of random dustbins.");
    return;
  }

  var data = {
    numDustbins: numDustbins,
  };

  fetch("/add_random_dustbins", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then(function (response) {
      if (response.status === 201) {
        alert(numDustbins + " random dustbins added successfully!");
        loadDustbins();
      } else {
        alert("Failed to add random dustbins.");
      }
    })
    .catch(function (error) {
      alert("An error occurred: " + error);
    });
}

function calculateOptimizedRoute() {
  fetch("/dustbins")
    .then(function (response) {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error("Failed to fetch dustbins.");
      }
    })
    .then(function (data) {
      var dustbins = data.dustbins;
      var dustbinsWithCoords = dustbins.filter(function (dustbin) {
        return dustbin.latitude && dustbin.longitude;
      });
      var dustbinsCoords = dustbinsWithCoords.map(function (dustbin) {
        return [parseFloat(dustbin.longitude), parseFloat(dustbin.latitude)]; // Ensure [longitude, latitude] format
      });
      var requestData = {
        dustbins: dustbinsWithCoords,
        num_vehicles: 5,
      };
      fetch("http://127.0.0.1:5000/plan_optimized_route", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      })
        .then(function (response) {
          if (response.ok) {
            return response.json();
          } else {
            throw new Error("Failed to calculate optimized route.");
          }
        })
        .then(function (data) {
          var routes = data.optimized_routes;
          var colors = [
            "red",
            "blue",
            "green",
            "orange",
            "purple",
            "yellow",
            "cyan",
            "magenta",
            "lime",
            "pink",
          ]; // Colors for different routes

          routes.forEach(function (route, index) {
            var routeCoords = route.map(function (routeIndex) {
              return dustbinsCoords[routeIndex];
            });

            var routeSequence = route.join(" -> ");
            document.getElementById("optimizedRouteSequence").textContent +=
              "Vehicle " + (index + 1) + ": " + routeSequence + "\n";

            // Use Mapbox Directions API to get detailed route
            var waypoints = routeCoords
              .map(function (coord) {
                return coord.join(",");
              })
              .join(";");

            var url = `https://api.mapbox.com/directions/v5/mapbox/driving-traffic/${waypoints}?geometries=geojson&access_token=sk.eyJ1IjoiYmhhcmFkaHdhajE4IiwiYSI6ImNtM2NveGVtYjF0M2gya3F4dzhoYnpuOG0ifQ.Nbi-vp9KifmkJ5e_wfP0Wg`;

            fetch(url)
              .then(function (response) {
                if (response.ok) {
                  return response.json();
                } else {
                  throw new Error("Failed to fetch route from Mapbox.");
                }
              })
              .then(function (data) {
                var routeGeoJSON = data.routes[0].geometry;
                var routePolyline = L.geoJSON(routeGeoJSON, {
                  style: {
                    color: colors[index % colors.length],
                    weight: 4,
                  },
                }).addTo(map);
                map.fitBounds(routePolyline.getBounds());
              })
              .catch(function (error) {
                alert(
                  "An error occurred while fetching the route: " + error.message
                );
              });
          });
        })
        .catch(function (error) {
          alert(
            "An error occurred while calculating the optimized route: " +
              error.message
          );
        });
    })
    .catch(function (error) {
      alert("An error occurred while fetching dustbins: " + error.message);
    });
}

function loadDustbins() {
  fetch("/dustbins")
    .then(function (response) {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error("Failed to fetch dustbins.");
      }
    })
    .then(function (data) {
      var dustbinsContainer = document.getElementById("dustbinsContainer");
      dustbinsContainer.innerHTML = "";

      // Define custom icon for the depot using leaflet.awesome-markers
      var depotIcon = L.icon({
        iconUrl: "/assets/home.png", // Path to your custom red marker icon
        iconSize: [30, 51], // Size of the icon
        iconAnchor: [12, 41], // Point of the icon which will correspond to marker's location
        popupAnchor: [1, -34], // Point from which the popup should open relative to the iconAnchor
        // shadowUrl:
        //   "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png", // Optional shadow image
        shadowSize: [41, 41], // Size of the shadow
      });

      data.dustbins.forEach(function (dustbin, index) {
        var dustbinElement = document.createElement("div");
        dustbinElement.classList.add("dustbin");
        dustbinElement.innerHTML = `
          <p><strong>ID:</strong> ${dustbin.id}
          <strong>Latitude:</strong> ${dustbin.latitude}
          <strong>Longitude:</strong> ${dustbin.longitude}
          <strong>Capacity:</strong> ${dustbin.capacity}
          <button onclick="modifyDustbin(${dustbin.id})">Modify</button>
          <button onclick="deleteDustbin(${dustbin.id})">Delete</button></p>
        `;
        dustbinsContainer.appendChild(dustbinElement);

        // Add markers to the map with labels from the server
        var marker;
        var dustbinIcon = L.icon({
          iconUrl: "/assets/dustbin.png", // Path to your dustbin logo image
          iconSize: [25, 40], // Size of the icon (adjust as needed)
          iconAnchor: [12, 41], // Anchor point of the icon (adjust as needed)
          popupAnchor: [1, -34],
          // Position of the popup (adjust as needed)
        });
        if (index === 0) {
          // Use custom icon for the depot
          marker = L.marker([dustbin.latitude, dustbin.longitude], {
            icon: depotIcon,
          }).addTo(map);
        } else {
          // Use default marker for other dustbins
          var marker = L.marker([dustbin.latitude, dustbin.longitude], {
            icon: dustbinIcon,
          }).addTo(map);
        }
        marker.bindPopup("ID: " + dustbin.id); // Add ID label to the marker
      });
    })
    .catch(function (error) {
      alert("An error occurred: " + error);
    });
}

function modifyDustbin(id) {
  var latitude = prompt("Enter new latitude:");
  var longitude = prompt("Enter new longitude:");
  var capacity = prompt("Enter new capacity:");

  if (latitude !== null && longitude !== null && capacity !== null) {
    var data = {
      latitude: latitude,
      longitude: longitude,
      capacity: capacity,
    };

    fetch(`http://127.0.0.1:5000/update_dustbin/${id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then(function (response) {
        if (response.ok) {
          alert("Dustbin modified successfully!");
          loadDustbins();
        } else {
          throw new Error("Failed to modify dustbin.");
        }
      })
      .catch(function (error) {
        alert("An error occurred: " + error);
      });
  }
}

function deleteDustbin(id) {
  if (confirm("Are you sure you want to delete this dustbin?")) {
    fetch(`http://127.0.0.1:5000/delete_dustbin/${id}`, {
      method: "DELETE",
    })
      .then(function (response) {
        if (response.ok) {
          alert("Dustbin deleted successfully!");
          loadDustbins(); // Reload dustbins after deletion
        } else {
          throw new Error("Failed to delete dustbin.");
        }
      })
      .catch(function (error) {
        alert("An error occurred: " + error);
      });
  }
}

function clearAllDustbins() {
  if (confirm("Are you sure you want to clear all dustbins?")) {
    fetch("/clear_all_dustbins", {
      method: "DELETE",
    })
      .then(function (response) {
        if (response.ok) {
          alert("All dustbins cleared successfully!");
          loadDustbins(); // Reload dustbins after clearing
        } else {
          throw new Error("Failed to clear dustbins.");
        }
      })
      .catch(function (error) {
        alert("An error occurred: " + error);
      });
  }
}

function clearFields() {
  document.getElementById("latitude").value = "";
  document.getElementById("longitude").value = "";
  document.getElementById("capacity").value = "";
}

const depotIcon = L.icon({
  iconUrl: depotIconPath, // Path to your custom red marker icon
  iconSize: [25, 41], // Size of the icon
  iconAnchor: [12, 41], // Point of the icon which will correspond to marker's location
  popupAnchor: [1, -34], // Point from which the popup should open relative to the iconAnchor
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png", // Optional shadow image
  shadowSize: [41, 41], // Size of the shadow
});

var map = L.map("map").setView([12.909354, 77.566596], 14);

// Add OpenStreetMap tile layer to the map
L.tileLayer(
  "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=sk.eyJ1IjoiYmhhcmFkaHdhajE4IiwiYSI6ImNtM2NveGVtYjF0M2gya3F4dzhoYnpuOG0ifQ.Nbi-vp9KifmkJ5e_wfP0Wg",
  {
    attribution:
      'Map data © <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: "mapbox/streets-v11",
    tileSize: 512,
    zoomOffset: -1,
    accessToken:
      "sk.eyJ1IjoiYmhhcmFkaHdhajE4IiwiYSI6ImNtM2NveGVtYjF0M2gya3F4dzhoYnpuOG0ifQ.Nbi-vp9KifmkJ5e_wfP0Wg",
  }
).addTo(map);
