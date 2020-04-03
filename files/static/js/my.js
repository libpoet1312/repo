let tags = [];
let categories = [];
let areas = [];
let text_search;

// FUNCTION'S AREA ///

function createTree(jsonData, tree) {
    let parsedJson = $.parseJSON(jsonData);
    console.log(parsedJson);

    $(tree).jstree({
        core: {
            themes: {
                name: 'proton',
                responsive: true,
                dots: false,
                icons: false,
            },
            check_callback: !0,
            data: parsedJson
        },
        'search': {
            "case_insensitive": true,
            "show_only_matches" : true,
            "show_only_matches_children": true
        },
        checkbox:{},
        plugins: ['search', "types", "checkbox", 'changed', 'wholerow']
    }).on('search.jstree', function (nodes, str, res) {
        // console.log(str);
        if (str.nodes.length===0) {
            $(tree).jstree(true).hide_all();
        }
    });
}

function Ajax(){
    $.ajax({
            async : true,
            type : "GET",
            url : '',
            dataType : "json",
            traditional : true,
            data: {
                tags : tags,
                categories: categories,
                areas: areas,
                text_search: text_search
            },

            success : function(json) {
                $('#list').html(json)
            },

            error : function(xhr, ajaxOptions, thrownError) {
                alert(xhr.status);
                alert(thrownError);
            }
        });

}

function Reset(){
    categories = [];
    text_search = '';
    tags = [];
    $(":checkbox").each(function () {
        $(this).prop("checked", false);
        console.log($(this));
    });

    areas = [];

    Ajax();
}

/// DOM READY AREA ///
$(document).ready( function () {
    //////////////
    /// JSTREES ///
    //////////////
    $(function() {
        const script = document.getElementById('myscript');
        const caturl = script.getAttribute('caturl');
        const areaurl = script.getAttribute('areaurl');

        const categorytree = document.getElementById('Cattree');
        const areatree = document.getElementById('Areatree');



        // CATEGORY TREE
        $.ajax({
            async : true,
            type : "GET",
            url : caturl,
            dataType : "json",
            traditional : true,


            success : function(json) {
                // console.log("Call trigger");
                const dataset = json;

                createTree(dataset, categorytree);
            },

            error : function(xhr, ajaxOptions, thrownError) {
                alert(xhr.status);
                alert(thrownError);
            }
        });

        // AREA TREE
        $.ajax({
            async : true,
            type : "GET",
            url : areaurl,
            dataType : "json",
            traditional : true,


            success : function(json) {
                // console.log("Call trigger");

                var dataset = json;
                // console.log(dataset);

                createTree(dataset, areatree);
            },

            error : function(xhr, ajaxOptions, thrownError) {
                alert(xhr.status);
                alert(thrownError);
            }
        });
    });

    // ALWAYS load from selectors the checkbox and reload
    const tagscheckbox = document.querySelectorAll("input[type=checkbox]");
    tagscheckbox.forEach( (item, i) => {
        if(item.checked === true){
            tags.push(item.value)
        }
    });
    console.log(tags);
    if( tags.length ){
        // AJAX CALL
        console.log('from reload');
        Ajax()
    }

    /// CATEGORY
    /// TREE SEARCH
    ///
    $('#cattreesearch').keyup(function(){

        // console.log($(this).val());


        $('#Cattree').jstree(true).show_all();
        $('.jstree-node').show();
        $('#Cattree').jstree('search', $(this).val());
        $('.jstree-hidden').hide();
        $('a.jstree-search').parent('li').find('.jstree-hidden').show();
    });


    //                   //
    //  EVENT LISTENERS  //
    //                   //


    // DROPDOWN TAGs
    $(document).on('click', '.tags', function() {
        var span = document.getElementsByClassName('caret-icon');
        var submenu = document.getElementById('tagmenu');

        submenu.classList.toggle('show');
        submenu.style.display = submenu.style.display === "block" ? "none" : "block"; //dropdown
        $(span).toggleClass('fa-caret-up fa-caret-down'); // caret up-down
    });

    // FILTER BY TEXT
    $('form').on('submit', function (e) {
        e.preventDefault();
        text_search = $('#text_search').val();
        console.log(text_search);
        Ajax();
    });

    // FILTER BY TAG
    $(document).on('click', "input[type=checkbox]", function() {
        // console.log($(this).prop("checked"));

        localStorage[$(this).val()] = $(this).prop("checked");
        // console.log(localStorage[$(this).val()]);

        // if checked
        if($(this).prop("checked")){
            if( !tags.includes($(this).val())){
            // put in array
                tags.push($(this).val());
                localStorage.setItem($(this).val(), $(this).prop("checked"));
            }
        }else{
            //remove from array
            const index = tags.indexOf($(this).val());
            if (index > -1) {
                tags.splice(index, 1);
                localStorage.setItem($(this).val(), $(this).prop("checked"));
            }
        }
        console.log('From input');
        console.log(tags);
        Ajax();
    });

    // RESET FILTERS
    $('form').on('reset', function (e) {
        Reset();
    });



    ///                 ///
    ///  CATEGORY TREE  ///
    ///     FILTER      ///

    // when clicked fetch the selected by name only!
    $('#Cattree').bind('changed.jstree', function (e, data) {
        // console.log(data);
        var checked = [];

        var checkedids = $('#Cattree').jstree('get_bottom_checked');
        if(checkedids){
            $.each(checkedids, (i, value) => {
                var path = $('#Cattree').jstree(true).get_path(value, '/');
                console.log(path);
                checked.push(path);
            });
        }else {
            checked =[];
        }
        categories = checked;
        // console.log(checked);
        Ajax();



        //console.log(data.changed.selected) //


    });






});


 // trigger move node event
 // $('#tree').on("move_node.jstree", function (e, data) {
 //
	//   $.ajax({
	//         async : true,
	//         type : "POST",
	//         url : "/inventory/move_node_ajax/",
	//         dataType : "json",
	// 		data : {'node_id': data.node.id, 'parent_id': data.node.parent, csrfmiddlewaretoken: '{{ csrf_token }}'},
	//         success : function(json) {
	//         	console.log("move trigger")
	//         },
 //
	//         error : function(xhr, ajaxOptions, thrownError) {
	//             alert(xhr.status);
	//             alert(thrownError);
	//         }
	//     });
	// });