

function changeText(id){    
   let allTaskBtn =  document.querySelectorAll('.btns')
   allTaskBtn = [...allTaskBtn]
    
    allTaskBtn.forEach(element => {
        // console.log(element.getAttribute('id') == id)
      if(element.getAttribute('id') == id){
        if(element.innerText == "End Task"){
            element.innerText = "Start Task"
        }else{
            element.innerText = "End Task"
        }
      }
    });
}

document.addEventListener('DOMContentLoaded' , function(){
    let allBtns = document.querySelectorAll('td.btnst')
    let allbtnTask = document.querySelectorAll('.btns')
    allBtns = [...allBtns] 
    allbtnTask = [...allbtnTask]
allBtns.forEach( (item , index) => {
   console.log(  item.getAttribute('data-id'))
   console.log(  item.innerText)

    if(item.innerText == "Completed"){
allbtnTask[index].innerText = "Start Task"
    }else{
allbtnTask[index].innerText = "End Task"
  }
})
    
})