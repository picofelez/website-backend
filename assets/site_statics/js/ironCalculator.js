$(document).ready(function () {
    function profile_calculator_formula(area, length, width, count) {
        let num = ((7.85 * length * width * area * 2) / 1000) * count
        return num.toFixed(2)
    }

    function rebar_calculator_formula(diameter, length, count) {
        let num = (((diameter / 2) * (diameter / 2) * length * 3.14 * 7.8) / 1000) * count
        return num.toFixed(2)
    }

    function foil_calculator_formula(length, width, thickness, count) {
        let num = (8 * thickness * length * width) * count
        return num.toFixed(2)
    }

    // initial state
    let profile_init = profile_calculator_formula(
        $('#profile_area').val(),
        $('#profile_length').val(),
        $('#profile_width').val(),
        $('#profile_count').val()
    )
    $('#profile_weight').val(`${profile_init} کیلوگرم`)

    let rebar_init = rebar_calculator_formula(
        $('#rebar_diameter').val(),
        $('#rebar_length').val(),
        $('#rebar_count').val()
    )
    $('#rebar_weight').val(`${rebar_init} کیلوگرم`)

    let foil_init = foil_calculator_formula(
        $('#foil_length').val(),
        $('#foil_width').val(),
        $('#foil_thickness').val(),
        $('#foil_count').val()
    )
    $('#foil_weight').val(`${foil_init} کیلوگرم`)
    $('#foil_total_price').val(`${(foil_init * $('#foil_price').val()).toLocaleString()} تومان`)

    // formula mode
    $('#formula_mode').change(function () {
        let val = $(this).val()
        if (val === 'foil') {
            $('#profile_calculator').hide(400)
            $('#rebar_calculator').hide(400)
            $('#foil_calculator').show(400)
            $('#foil_description').show(400)
        } else if (val === 'rebar') {
            $('#profile_calculator').hide(400)
            $('#rebar_calculator').show(400)
            $('#foil_calculator').hide(400)
            $('#foil_description').hide(400)
        } else if (val === 'profile') {
            $('#profile_calculator').show(400)
            $('#rebar_calculator').hide(400)
            $('#foil_calculator').hide(400)
            $('#foil_description').hide(400)
        }
    })

    // profile calculator
    $("#profile_area").change(function () {
        let formula = profile_calculator_formula(
            $('#profile_area').val(),
            $('#profile_length').val(),
            $('#profile_width').val(),
            $('#profile_count').val()
        )
        $('#profile_weight').val(`${formula} کیلوگرم`)
    })

    $("#profile_length").change(function () {
        let formula = profile_calculator_formula(
            $('#profile_area').val(),
            $('#profile_length').val(),
            $('#profile_width').val(),
            $('#profile_count').val()
        )
        $('#profile_weight').val(`${formula} کیلوگرم`)
    })

    $("#profile_width").change(function () {
        let formula = profile_calculator_formula(
            $('#profile_area').val(),
            $('#profile_length').val(),
            $('#profile_width').val(),
            $('#profile_count').val()
        )
        $('#profile_weight').val(`${formula} کیلوگرم`)
    })

    $("#profile_count").change(function () {
        let formula = profile_calculator_formula(
            $('#profile_area').val(),
            $('#profile_length').val(),
            $('#profile_width').val(),
            $('#profile_count').val()
        )
        $('#profile_weight').val(`${formula} کیلوگرم`)
    })

    // rebar calculator
    $('#rebar_diameter').change(function () {
        let num = rebar_calculator_formula(
            $('#rebar_diameter').val(),
            $('#rebar_length').val(),
            $('#rebar_count').val()
        )
        $('#rebar_weight').val(`${num} کیلوگرم`)
    })

    $('#rebar_length').change(function () {
        let num = rebar_calculator_formula(
            $('#rebar_diameter').val(),
            $('#rebar_length').val(),
            $('#rebar_count').val()
        )
        $('#rebar_weight').val(`${num} کیلوگرم`)
    })

    $('#rebar_count').change(function () {
        let num = rebar_calculator_formula(
            $('#rebar_diameter').val(),
            $('#rebar_length').val(),
            $('#rebar_count').val()
        )
        $('#rebar_weight').val(`${num} کیلوگرم`)
    })

    // foil calculator
    $('#foil_length').change(function () {
        let num = foil_calculator_formula(
            $('#foil_length').val(),
            $('#foil_width').val(),
            $('#foil_thickness').val(),
            $('#foil_count').val()
        )
        $('#foil_weight').val(`${num} کیلوگرم`)
        $('#foil_total_price').val(`${(num * $('#foil_price').val()).toLocaleString()} تومان`)
    })

    $('#foil_width').change(function () {
        let num = foil_calculator_formula(
            $('#foil_length').val(),
            $('#foil_width').val(),
            $('#foil_thickness').val(),
            $('#foil_count').val()
        )
        $('#foil_weight').val(`${num} کیلوگرم`)
        $('#foil_total_price').val(`${(num * $('#foil_price').val()).toLocaleString()} تومان`)
    })

    $('#foil_thickness').change(function () {
        let num = foil_calculator_formula(
            $('#foil_length').val(),
            $('#foil_width').val(),
            $('#foil_thickness').val(),
            $('#foil_count').val()
        )
        $('#foil_weight').val(`${num} کیلوگرم`)
        $('#foil_total_price').val(`${(num * $('#foil_price').val()).toLocaleString()} تومان`)
    })

    $('#foil_count').change(function () {
        let num = foil_calculator_formula(
            $('#foil_length').val(),
            $('#foil_width').val(),
            $('#foil_thickness').val(),
            $('#foil_count').val()
        )
        $('#foil_weight').val(`${num} کیلوگرم`)
        $('#foil_total_price').val(`${(num * $('#foil_price').val()).toLocaleString()} تومان`)
    })

    $('#foil_price').change(function () {
        let num = foil_calculator_formula(
            $('#foil_length').val(),
            $('#foil_width').val(),
            $('#foil_thickness').val(),
            $('#foil_count').val()
        )
        $('#foil_weight').val(`${num} کیلوگرم`)
        $('#foil_total_price').val(`${(num * $('#foil_price').val()).toLocaleString()} تومان`)
    })
})