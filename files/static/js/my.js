let tags = [];
let categories = [];
let areas = [];
let text_search;
let page;

const areatree = $('#Areatree');
const categorytree = $('#Cattree');


// FUNCTION'S AREA ///

function createCATEGORYTree(jsonData, tree) {
    let parsedJson = $.parseJSON(jsonData);
    //console.log(parsedJson);

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

function createAREATree(jsonData, tree) {
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
        checkbox:{
            three_state: false,
            two_state: true,
            whole_node: true,
            tie_selection: true,
            "keep_selected_style": true
        },
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
                text_search: text_search,
                page: page,
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
    text_search = '';
    tags = [];
    $(":checkbox").each(function () {
        $(this).prop("checked", false);
        console.log($(this));
    });

    areas = [];
    areatree.jstree("deselect_all");



    categories = [];
    categorytree.jstree("deselect_all");

    Ajax();
}


$(document).on('click', '#prev', function(e) {
    e.preventDefault();
    page = ($( '#prev' )[0].href).split('=');
    console.log("Previous button Debuggin...", page);
    Ajax();
});

$(document).on('click', '#next', function(e) {

    e.preventDefault();
    page = ($( '#next' )[0].href).split('=');
    console.log("Next button Debuggin...", page);
    Ajax();
});

/// DOM READY AREA ///
$(document).ready( function () {

    //////////////
    /// JSTREES ///
    //////////////


    // create trees
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

                createCATEGORYTree(dataset, categorytree);
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

                createAREATree(dataset, areatree);
            },

            error : function(xhr, ajaxOptions, thrownError) {
                alert(xhr.status);
                alert(thrownError);
            }
        });
    });

    /*
    *
    *       GET AREA FROM URL AND SELECT ATTRIBUTE
    *       THEN IT WILL AUTOMATICALLY CALL THE EVENT AND THEN AJAX
    *
    * */
    areatree.on('ready.jstree', function () {
        let pathArray = window.location.pathname.split('/');
        console.log('pathArray= ', pathArray[2]);

        let instance = areatree.jstree(true);
        // console.log('tree instance ', instance);

        let nodes = instance._model.data;

        $.each(nodes, function (index, node) {
            let original = node.original;
            if(original !== undefined){
                // console.log('slug', original.slug);
                if(original.slug && original.slug === pathArray[2]) {
                    instance.select_node(node);
                    return false;
                }

            }
        });
    });



    // load from selectors the checkbox and reload
    const tagscheckbox = document.querySelectorAll("input[type=checkbox]");
    tagscheckbox.forEach( (item, i) => {
        if(item.checked === true){
            tags.push(item.value)
        }
    });

    // always call ajax when ready document
    Ajax();




    /// CATEGORY
    /// TREE SEARCH
    $('#cattreesearch').keyup(function(){

        categorytree.jstree(true).show_all();
        $('.jstree-node').show();
        categorytree.jstree('search', $(this).val());
        $('.jstree-hidden').hide();
        $('a.jstree-search').parent('li').find('.jstree-hidden').show();
    });

    /// CATEGORY
    /// TREE SEARCH
    $('#areatreesearch').keyup(function(){

        areatree.jstree(true).show_all();
        $('.jstree-node').show();
        areatree.jstree('search', $(this).val());
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


    ///  CATEGORY TREE  ///
    ///     FILTER      ///
    categorytree.bind('changed.jstree', function (e, data) {
        var checked = [];

        var checkedids = categorytree.jstree('get_bottom_checked');
        if(checkedids){
            $.each(checkedids, (i, value) => {
                var path = categorytree.jstree(true).get_path(value, '/');
                // console.log(path);
                checked.push(path);
            });
        }else {
            checked =[];
        }
        categories = checked;
        // console.log(checked);
        Ajax();

    });


    ///    AREA TREE    ///
    ///     FILTER      ///
    areatree.bind('select_node.jstree  deselect_node.jstree', function (e, data) {
        // console.log(data);

        const cur = data.node;
        const parent = areatree.jstree(true).get_parent(cur); // id of parent
        const parentobj = data.instance.get_node(data.node.parent);
        // console.log('parentobj= ', parentobj);

        const siblings = areatree.jstree(true).get_children_dom(parentobj); // get cur siblings
        const children = areatree.jstree(true).get_children_dom(cur); // get children



        if(areatree.jstree(true).is_parent(cur)){
            areatree.jstree(true).toggle_node(cur); // toggle full tree of node
        }
        const path = areatree.jstree(true).get_path(cur, '/');
        // console.log(path);
        let put = false;

        //first is always parent node
        if(areas.length===0){
            if(e.type==='select_node'){
                const index = areas.indexOf(path);
                if (index === -1){
                    areas.push(path);
                }
            }
        }else{
            // more than one in areas
            // most cases here

            if( parent === '#') {
                // is parent
                if (e.type === 'select_node') {
                    areas.push(path);
                } else {


                    //uncheck ALL CHILDREN
                    $.each(children, (i, child) => {
                        const index = areas.indexOf(areatree.jstree(true).get_text(child));
                        if (index > -1) {
                            areas.splice(index, 1);
                        }
                        areatree.jstree(true).uncheck_node(child);
                    });

                    const index = areas.indexOf(path);
                    console.log(index);
                    if (index > -1) {
                        areas.splice(index, 1);
                    }
                }
            }else{
                // is child
                if (e.type === 'select_node') {
                    $.each(areas, function (i, area) {
                       if(path.includes(area)){
                           // console.log(area, ' of ', path);
                           areas[i] = path;
                           put = true;
                       }
                    });
                    if(!put){
                        areas.push(path);
                    }
                }else{
                    // delete
                    const index = areas.indexOf(path);
                    if (index > -1) {
                        areas.splice(index, 1);
                    }
                    let c = false;
                    $.each(siblings, function (i, sibling) {
                        if(areatree.jstree(true).is_selected(sibling)){
                            c = true;
                        }
                    });
                    if(!c){
                        areas.push(parentobj.text)
                    }
                }
            }
        }
        console.log('areas=  ',areas);
        Ajax();

    });

    // RESET FILTERS
    $('form').on('reset', function (e) {
        Reset();
    });



});


