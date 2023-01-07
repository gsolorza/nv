function formHasData(elements, form_group) {
    let inputHasData = []
    for (element of elements) { 
        let input = form_group.querySelector(element).children[0].firstElementChild.children[1];
        if (input.value) {
            inputHasData.push(true)
        }
        // Substracting one from the array because the delete button does not have input value so we have to remove that element from the validation
        if (inputHasData.length > 4) {
            return true
        }
    }
    return false  
}


function updateForm(section) { 
    let formName = section.split("_")[2];
    let form_group = document.querySelector(section);
    if (!formHasData(elementList[formName], form_group)) {
        form_group.setAttribute("hidden", "")
        for (element of elementList[formName]) {
            field = form_group.querySelector(element).children[0].firstElementChild.children[1]
            field.setAttribute("disabled", "")
        }
    }
    
}

window.onload = function () {
    section_list = ["#form_section_cisco_0", "#form_section_vendor_0", "#form_section_software_0"]
    for (section of section_list) { 
        updateForm(section)
    }
}

