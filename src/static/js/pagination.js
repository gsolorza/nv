const paginationNumbers = document.getElementById("pagination-numbers");
const paginatedList = document.getElementById("table_body");
let listItems = paginatedList.querySelectorAll("tr");
const nextButton = document.getElementById("next-button");
const prevButton = document.getElementById("prev-button");

let paginationMinRange = 0
let paginationMaxRange = 10

const paginationLimit = 5;
let pageCount = Math.ceil(listItems.length / paginationLimit);
let currentPage;
let pageDifference;

function isBetween(index, min, max) {
  return (index >= min && index <= max) || (index >= max && index <= min);
}

const appendPageNumber = (index) => {
  const pageNumber = document.createElement("button");
  pageNumber.className = "pagination-number";
  pageNumber.innerHTML = index;
  pageNumber.setAttribute("page-index", index);
  pageNumber.setAttribute("aria-label", "Page " + index);
  
  if (!isBetween(index, paginationMinRange, paginationMaxRange))
    pageNumber.setAttribute("hidden", true)

  paginationNumbers.appendChild(pageNumber);
  };
  
const getPaginationNumbers = () => {
    paginationNumbers.innerHTML = ""
    for (let i = 1; i <= pageCount; i++) {
      appendPageNumber(i);
    }
    document.querySelectorAll(".pagination-number").forEach((button) => {
      const pageIndex = Number(button.getAttribute("page-index"));
      if (pageIndex) {
        button.addEventListener("click", () => {
          setCurrentPage(pageIndex);
        });
  
      }
  
    });
};

const handleActivePageNumber = () => {
    document.querySelectorAll(".pagination-number").forEach((button) => {
      button.classList.remove("active");
      const pageIndex = Number(button.getAttribute("page-index"));
      if (pageIndex == currentPage) {
        button.classList.add("active");
      }
  
    });
  
};

const disableButton = (button) => {
  button.classList.add("disabled");
  button.setAttribute("disabled", true);
};

const enableButton = (button) => {
  button.classList.remove("disabled");
  button.removeAttribute("disabled");
};

const handlePageButtonsStatus = () => {
  if (currentPage === 1) {
    disableButton(prevButton);
  } else {
    enableButton(prevButton);
  }
  if (pageCount === currentPage) {
    disableButton(nextButton);
  } else {
    enableButton(nextButton);
  }
};

const setCurrentPage = (pageNum) => {
  console.log(`Current Page ${currentPage}`)
  console.log(`Page Number ${pageNum}`)
  if (pageNum >= paginationMaxRange) {
    paginationMinRange += 10
    paginationMaxRange += 10
    getPaginationNumbers();
  }
  else if (pageNum <= paginationMinRange){
    paginationMinRange -= 10
    paginationMaxRange -= 10
    getPaginationNumbers();
  }
  currentPage = pageNum;
  handleActivePageNumber();
  handlePageButtonsStatus();
  const prevRange = (pageNum - 1) * paginationLimit;
  const currRange = pageNum * paginationLimit;
  
  console.log(`Current Range ${currRange}`)
  console.log(`Previous Range ${prevRange}`)
  listItems.forEach((item, index) => {
    item.setAttribute("hidden", "");
    if (index >= prevRange && index < currRange) {
      item.removeAttribute("hidden");
    }
  });
};

const onClickPagination = () => {

  prevButton.addEventListener("click", () => {
      setCurrentPage(currentPage - 1);
    });
  nextButton.addEventListener("click", () => {
      setCurrentPage(currentPage + 1);
    });
}

const displayFormCount = () => { 
  p = document.createElement("p")
  p.className = "text-center"
  p.innerText = `Total Number of Checklist: ${listItems.length}`
  document.querySelector("#forms-total-number").appendChild(p)
}

window.addEventListener("load", () => {
  getPaginationNumbers();
  setCurrentPage(1);
  onClickPagination();
  displayFormCount();
});


  






  
