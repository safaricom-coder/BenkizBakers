import {gridifyTablePlace,unGridifyTablePlace,coverEverything,lids} from 'benkizmain.js'
let modifyAccountButtons = document.querySelectorAll('.modifyAccountButton')

let gridContainer = document.getElementById('grid-container')

modifyAccountButtons.forEach((modifyAccountButton)=>{
    modifyAccountButton.addEventListener('click',()=>{
        if(gridContainer.classList.contains('grid-container')){
            coverEverything()
            gridContainer.classList.remove('hidden')
            gridifyTablePlace()
        }else{
            gridContainer.classList.add('hidden')
            unGridifyTablePlace()
        }
    })
})
