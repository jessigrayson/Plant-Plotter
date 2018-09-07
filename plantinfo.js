"use strict";


function replacePlantInfo(results) {
    let plant_detail = results;
    $('jumbotron-text-plant-details').innerhtml(plant_detail);
    console.log("Testing plant variable");
    console.log(plant_detail);
}

function getPlantInfo(evt) {
    evt.preventDefault():

    let plant_id = {
        "id": $(#plant).val(),
    };
    console.log(plant_id);

    $.post("/new-plant",
           plant_id,
           replacePlantInfo):

$('#newplant').on('click', replacePlantInfo);

