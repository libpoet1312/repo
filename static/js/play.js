if($('#Areatree').jstree(true).is_parent(node.node)){
            // PARENT NODE

            $('#Areatree').jstree(true).toggle_node(node.node); // toggle full tree of node

            var children = $('#Areatree').jstree(true).get_children_dom(node.node); // get children


            if(e.type==='select_node'){
                $.each(children, (i, child) => {
                    // console.log($('#Areatree').jstree(true).get_text(child));
                    areas.push($('#Areatree').jstree(true).get_text(child));
                });
            }else {
                $.each(children, (i, child) => {
                    const index = areas.indexOf($('#Areatree').jstree(true).get_text(child));
                    if (index > -1) {
                        areas.splice(index, 1);
                    }
                    $('#Areatree').jstree(true).uncheck_node(child); //uncheck ALL CHILDREN
                });
            }
        }else{
            // CHILD NODE
            console.log('NODE NODE= ',node.node);
            const parent = $('#Areatree').jstree(true).get_prev_dom(node.node, false);
            // console.log('PARENT', parent, $('#Areatree').jstree(true).is_checked(parent));

            var children = $('#Areatree').jstree(true).get_children_dom(parent); // get children

            if(e.type==='select_node'){
                $.each(children, (i, child) => {
                    // console.log('CHILD = ',child);
                    if(child.id != node.node.id){
                        const index = areas.indexOf($('#Areatree').jstree(true).get_text(child));
                        if (index > -1) {
                            areas.splice(index, 1);
                        }
                    }
                    // areas.push('areas= ',node.node.text);
                });
                // console.log('areas00=  ',areas);
            }else{
                const index = areas.indexOf(node.node.text);
                console.log('deselect',node.node.text, index);
                if (index > -1) {
                    areas.splice(index, 1);
                }

                if($('#Areatree').jstree(true).is_checked(parent)){
                    $.each(children, (i, child) => {
                        // console.log($('#Areatree').jstree(true).get_text(child));
                        areas.push($('#Areatree').jstree(true).get_text(child));
                    });
                }
            }




        };