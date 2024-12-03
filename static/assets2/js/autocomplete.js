$(function() {
    var availableSchools = [];

    // Function to load schools from the server
    function loadSchools() {
        $.getJSON('{{ url_for("load_schools") }}', function(data) { // Use Flask to generate the correct path
            availableSchools = data; // Load the array of school objects
            $("#name_hs").autocomplete({
                source: availableSchools.map(function(school) {
                    return school.name; // Use school names for autocomplete
                }),
                select: function(event, ui) {
                    var selectedSchool = ui.item.value;
                    // Find the selected school's address
                    var school = availableSchools.find(s => s.name === selectedSchool);
                    if (school) {
                        $("#address_hs").val(school.address); // Fill the address field
                    } else {
                        $("#address_hs").val(''); // Clear address if no match
                    }
                }
            });
        });
    }

    // Load schools when the page is ready
    loadSchools();

    $("form").on("submit", function(event) {
        event.preventDefault();

        var schoolName = $("#name_hs").val().trim();
        var schoolAddress = $("#address_hs").val().trim();

        if (schoolName && schoolAddress && !availableSchools.find(s => s.name.toLowerCase() === schoolName.toLowerCase())) {
            availableSchools.push({ name: schoolName, address: schoolAddress }); // Add new school object
            
            $.ajax({
                type: "POST",
                url: "{{ url_for('add_school') }}", // Use Flask to generate the correct path
                data: { school_name: schoolName, school_address: schoolAddress }, // Send both name and address
                success: function(response) {
                    console.log("School added:", response);
                    loadSchools(); // Reload the schools to include the newly added one
                },
                error: function(error) {
                    console.error("Error adding school:", error);
                }
            });
        }

        this.submit();
    });
});
