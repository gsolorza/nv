const paginationNumbers = document.getElementById("pagination-numbers");
const paginatedList = document.getElementById("table_body");
let listItems = paginatedList.querySelectorAll("tr");
const nextButton = document.getElementById("next-button");
const prevButton = document.getElementById("prev-button");

const paginationLimit = 5;
let pageCount = Math.ceil(listItems.length / paginationLimit);
let currentPage;

const appendPageNumber = (index) => {
    const pageNumber = document.createElement("button");
    pageNumber.className = "pagination-number";
    pageNumber.innerHTML = index;
    pageNumber.setAttribute("page-index", index);
    pageNumber.setAttribute("aria-label", "Page " + index);
    paginationNumbers.appendChild(pageNumber);
  };
  
const getPaginationNumbers = () => {
    for (let i = 1; i <= pageCount; i++) {
      appendPageNumber(i);
    }
  
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

const setCurrentPage = (pageNum) => {
    currentPage = pageNum;
    handleActivePageNumber();
    const prevRange = (pageNum - 1) * paginationLimit;
    const currRange = pageNum * paginationLimit;
  
    listItems.forEach((item, index) => {
      item.setAttribute("hidden", "");
      if (index >= prevRange && index < currRange) {
        item.removeAttribute("hidden");
      }
    });
  };

const onClickPagination = () => {
    document.querySelectorAll(".pagination-number").forEach((button) => {
        const pageIndex = Number(button.getAttribute("page-index"));
        if (pageIndex) {
          button.addEventListener("click", () => {
            setCurrentPage(pageIndex);
          });
    
        }
    
      });
}


window.addEventListener("load", () => {
    getPaginationNumbers();
    setCurrentPage(1);
    onClickPagination();
});


  






  
