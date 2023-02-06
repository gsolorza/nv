var tableBody = document.querySelector("#table_body")
var search = document.querySelector("#search")

forms.sort(function (a, b) {
  var a = new Date(a.date)
  var b = new Date(b.date)
  return b - a
})

function formatDate(date){ 
  var newDate = new Date(date)
  var day = newDate.getDate()
  var month = newDate.getMonth() + 1
  var year = newDate.getFullYear()
  return `${day}/${month}/${year}`
}

function findTableMatch(searchWord, values){
  for(value of values){
    if(value && value.toLowerCase().startsWith(searchWord.toLowerCase()))
      return true
  }
  return false
}

function initTableForm() {
  tableBody.innerHTML = ""
    for(form of forms){
      let tr = document.createElement("tr")
      let td = document.createElement("td")
      let tdForm = document.createElement("form")
      tdForm.className = "container"
      tdForm.method = "GET"
      tdForm.action = `/form/${form.id}`
      let button = document.createElement("button")
      button.className = "btn btn-outline-primary"
      button.innerText = "VIEW"
      button.type = "submit"
      tr.innerHTML += `<td>${form.client_manager_name}</td>`
      tr.innerHTML += `<td>${form.pre_sales_name}</td>`
      tr.innerHTML += `<td>${form.customer_name}</td>`
      tr.innerHTML += `<td>${form.sales_force_id}</td>`
      tr.innerHTML += `<td>${form.quote_direct}</td>`
      tr.innerHTML += `<td>${form.purchase_order}</td>`
      tr.innerHTML += `<td>${formatDate(form.date)}</td>`
      if(form.status == "Completed")
        tr.innerHTML += `<td class="badge bg-success mt-3"> ${form.status} </td>`
      else
        tr.innerHTML += `<td>${form.status}</td>`
      td.appendChild(tdForm)
      tdForm.appendChild(button)
      tr.appendChild(td)
      tableBody.appendChild(tr)
    }
}

function updateTableForm(searchWord) {
  if (!searchWord) { 
    tableBody.innerHTML = ""
      for(form of forms){
        let tr = document.createElement("tr")
        let td = document.createElement("td")
        let tdForm = document.createElement("form")
        tdForm.className = "container"
        tdForm.method = "GET"
        tdForm.action = `/form/${form.id}`
        let button = document.createElement("button")
        button.className = "btn btn-outline-primary"
        button.innerText = "VIEW"
        button.type = "submit"
        tr.innerHTML += `<td>${form.client_manager_name}</td>`
        tr.innerHTML += `<td>${form.pre_sales_name}</td>`
        tr.innerHTML += `<td>${form.customer_name}</td>`
        tr.innerHTML += `<td>${form.sales_force_id}</td>`
        tr.innerHTML += `<td>${form.quote_direct}</td>`
        tr.innerHTML += `<td>${form.purchase_order}</td>`
        tr.innerHTML += `<td>${formatDate(form.date)}</td>`
        if(form.status == "Completed")
          tr.innerHTML += `<td class="badge bg-success mt-3"> ${form.status} </td>`
        else
          tr.innerHTML += `<td>${form.status}</td>`
        td.appendChild(tdForm)
        tdForm.appendChild(button)
        tr.appendChild(td)
        tableBody.appendChild(tr)
      }
  }
  else if (searchWord) {
    tableBody.innerHTML = ""
    for (form of forms) {
      if(findTableMatch(searchWord, Object.values(form))){
        let tr = document.createElement("tr")
        let td = document.createElement("td")
        let tdForm = document.createElement("form")
        tdForm.className = "container"
        tdForm.method = "GET"
        tdForm.action = `/form/${form.id}`
        let button = document.createElement("button")
        button.className = "btn btn-outline-primary"
        button.innerText = "VIEW"
        button.type = "submit"
        tr.innerHTML += `<td>${form.client_manager_name}</td>`
        tr.innerHTML += `<td>${form.pre_sales_name}</td>`
        tr.innerHTML += `<td>${form.customer_name}</td>`
        tr.innerHTML += `<td>${form.sales_force_id}</td>`
        tr.innerHTML += `<td>${form.quote_direct}</td>`
        tr.innerHTML += `<td>${form.purchase_order}</td>`
        tr.innerHTML += `<td>${formatDate(form.date)}</td>`
        if(form.status == "Completed")
          tr.innerHTML += `<td class="badge bg-success mt-3 "> ${form.status} </td>`
        else
          tr.innerHTML += `<td>${form.status}</td>`
        td.appendChild(tdForm)
        tdForm.appendChild(button)
        tr.appendChild(td)
        tableBody.appendChild(tr)
      }
    }
  }
  listItems = paginatedList.querySelectorAll("tr");
  pageCount = Math.ceil(listItems.length / paginationLimit);
  paginationMinRange = 0
  paginationMaxRange = 10
  paginationNumbers.innerHTML = ""
  getPaginationNumbers();
  setCurrentPage(1);
}

search.addEventListener("keyup", () => {
  searchWord = search.value;
  updateTableForm(searchWord);
})

initTableForm()