// variable that keeps all the filter information

var send_data = {}

$(document).ready(function () {
    // reset all parameters on page load

    resetFilters();
    // bring all the data without any filters

    getAPIData();
    // get all courses from database via
    // AJAX call into courses select options
    getCourses();
    getTags();

    // on filtering the course input
    $('#course').on('change', function () {
        // get the api data of updated variety

        if(this.value == "all")
            send_data['course'] = "";
        else
            send_data['course'] = this.value;
        getAPIData();
    });

    // on filtering the variety input
    $('#tag').on('change', function () {
        // get the api data of updated variety

        if(this.value == "all")
            send_data['tag'] = "";
        else
            send_data['tag'] = this.value;
        getAPIData();
    });
})

/**
    Function that resets all the filters
**/
function resetFilters() {
    $("#course").val("all");
    $("#tag").val("all");
}

function getAPIData() {
    let url = $('#list_data').attr("url")
    $.ajax({
        method: 'GET',
        url: url,
        data: send_data,
        beforeSend: function(){
            $("#no_results h5").html("Loading data...");
        },
        success: function (result) {
            putTableData(result);
        },
        error: function (response) {
            $("#no_results h5").html("Something went wrong");
            $("#list_data").hide();
        }
    });
}

function getCourses() {
    // fill the options of countries by making ajax call

    // obtain the url from the countries select input attribute

    let url = $("#course").attr("url");

    // makes request to getCountries(request) method in views

    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {

            countries_option = "<option value='all' selected>All Countries</option>";
            $.each(result["countries"], function (a, b) {
                countries_option += "<option>" + b + "</option>"
            });
            $("#countries").html(countries_option)
        },
        error: function(response){
            console.log(response)
        }
    });
}