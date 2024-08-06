// __author__ = "Patrick Nicolas"
// __copyright__ = "Copyright 2024. All rights reserved."

function getPermitOfficials() {
    document.addEventListener("DOMContentLoaded", function() {
        var permitOfficials = ["Official1", "Official2", "Official3", "Official4", "Official5"];

        var dropdown = document.getElementById("PermitOfficialDropdown");

        permitOfficials.forEach(function(permitOfficial) {
            var option = document.createElement("option");
            option.text = permitOfficial;
            option.value = permitOfficial.toLowerCase().replace(/\s+/g, '-'); // Optional: convert city name to lowercase hyphenated value
            dropdown.add(option);
        });
    });
}