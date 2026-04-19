const container = document.querySelector('.breadcrumb-option')
const navhumbergermenu = document.querySelector('.canvas__open')
const themeButtons = document.querySelectorAll('.themeButton')
const body = document.getElementById('documentBody') 

let is_set_dark_mode = JSON.parse(localStorage.getItem('is_set_dark_mode')) | false

function print(args){
    console.log(`${args}`)
}
// *********************handle theme*************************



function toggledarkenscreen(){
    is_set_dark_mode ? (is_set_dark_mode =false) : (is_set_dark_mode = true)
    if (is_set_dark_mode){
        body.classList.add('theme2')
        localStorage.setItem("is_set_dark_mode",JSON.stringify(false))
    }else {
        body.classList.remove("theme2")
        localStorage.setItem("is_set_dark_mode",JSON.stringify(true))
    }

}

toggledarkenscreen()

themeButtons.forEach((themeButton)=>{
    themeButton.addEventListener('click',()=>{
        toggledarkenscreen()
    })
})


// *********************handle theme*************************


let title = document.querySelector('.title').innerHTML
if ( container ){

    container.innerHTML = ''
    function updateContainer(pagename){
        let text = `
                    <div class="container">
                        <div class="row">
                            <div class="col-lg-6 col-md-6 col-sm-6">
                                <div class="breadcrumb__text">
                                    <h2>${pagename}</h2>
                                </div>
                            </div>
                            <div class="col-lg-6 col-md-6 col-sm-6">
                                <div class="breadcrumb__links">
                                    <a href={% url 'home' %}>Home</a>
                                    <span>${pagename}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                `
                container.innerHTML = text
    }
    updateContainer(title)
}


// handle table updaters appearing and disappering
document.addEventListener('DOMContentLoaded',()=>{
    let gridContainer = document.getElementById('grid-container')
    let addItemButton = document.getElementById('addItemButton')
    let addItemTable = document.querySelector('.form-container')
    let lids = document.querySelectorAll('.lid')
    let submitButtons = document.querySelectorAll('.submitbutton')

    let modifyItemButtons = document.querySelectorAll('.modifyItemButton')
    
    let itemsToModify = document.querySelectorAll('.itemToMod')

    function coverEverything(){
        itemsToModify.forEach((itemToModify)=>{
            if(!itemToModify.classList.contains('hidden')){
                itemToModify.classList.add('hidden')
            }else {
                while (itemToModify.classList.contains('hidden')){
                    itemToModify.classList.remove('hidden')
                }
                itemToModify.classList.add('hidden')
            }
        })
        if(!addItemTable.classList.contains('hidden')){
            addItemTable.classList.add('hidden')
        }
        lids.forEach((lid)=>{
            while (lid.classList.contains('hidden')){
                lid.classList.remove('hidden')
            }
            lid.classList.add('hidden')
        })
        

    }

    function gridifyTablePlace(){
        if(!gridContainer.classList.contains('grid-container')){
            gridContainer.classList.add('grid-container')
        }
    }

    function unGridifyTablePlace(){
        if(gridContainer.classList.contains('grid-container')){
            gridContainer.classList.remove('grid-container')
        }
    }
    
    addItemButton.addEventListener('click',()=>{
        if(addItemTable.classList.contains('hidden')){
            coverEverything()
            addItemTable.classList.remove('hidden')
            gridifyTablePlace()
            
        }else{
            
            addItemTable.classList.add('hidden')
            unGridifyTablePlace()
        }
    })

    modifyItemButtons.forEach(
        (modifyItemButton)=>{
            modifyItemButton.addEventListener('click',()=>{
                
                itemsToModify.forEach((itemToModify)=>{
                    if(itemToModify.id == modifyItemButton.id ){
                        if(itemToModify.classList.contains('hidden')){
                            coverEverything()
                            itemToModify.classList.remove('hidden')
                            gridifyTablePlace()
                        }else{
                            itemToModify.classList.add('hidden')
                            unGridifyTablePlace()
                        }

                    }
                })
            })
        }
    )



    submitButtons.forEach((submitButton)=>{
            submitButton.addEventListener('click',()=>{
                let namee=document.getElementById('namefield').value()
                let description=document.getElementById('textbody').value()
                let numberofitems=document.getElementById('numberitemfield').value()
                let category=document.getElementById('categoryfield').value()
                let price=document.getElementById("pricefield").value()

                let url = `http://127.0.0.1:8000/api/get/${submitButton.id}`
                            fetch(url,{
                                method:'PATCH',
                                'headers': {
                                    'Content-Type':'application/json',
                                    'X-CSRFToken':'{{csrf_token}}'
                                },
                                body:JSON.stringify(
                                            {
                                                "name": `${namee}`,
                                                "description": `${description}`,
                                                "price": `${price}`,
                                                "numberOfItems": `${numberofitems}`,
                                                "category": `${category}`
                                            }
                                )
                            }).then((response)=>{
                                return response.json
                            }).then(()=>{
                                window.location = "/adminpanel/itemmanager"
                            })
            })
        }
    )
    
    itemsToModify.forEach((itemToModify)=>{

        itemToModify.addEventListener('click',()=>{
            console.log(`Just kidding ${itemToModify.id}`)

        })
    })

})


// add and remove items from cart using increment and decrement signs

let cartItemCounts = document.querySelectorAll('.cartitemcount')
let cartAdditionButtons = document.querySelectorAll('.inc')
let cartRemoveButtons = document.querySelectorAll('.dec')



function getSpecificCartItemCount(id){
    let result = 0
    cartItemCounts.forEach((cartItemCount)=>{
        if (cartItemCount.id == id){
            result = Number(cartItemCount.innerHTML)
            
        }
    })
    return result
}
cartAdditionButtons.forEach((cartAdditionButton)=>{
    cartAdditionButton.addEventListener('click',()=>{
        let currentCartItemCount = getSpecificCartItemCount(cartAdditionButton.id)
        console.log(currentCartItemCount)
        let newNumberOfCartItems = 0
        newNumberOfCartItems= currentCartItemCount +=1
        console.log(newNumberOfCartItems)
        
        let url = `http://127.0.0.1:8000/api/getcartitem/${cartAdditionButton.id}`
        let urll = `https://safariocom.pythonanywhere.com/api/getcartitem/${cartAdditionButton.id}`
        fetch(url,{
            method:'PUT',
            'headers': {
                'Content-Type':'application/json',
                'X-CSRFToken':'{{csrf_token}}'
            },
            body:JSON.stringify(
                {
                    "quantity":newNumberOfCartItems
                }
            )
        }).then((response)=>{
            return response.json
        }).then(()=>{
            window.location = "/updatecart/"
        })
    })
        
})
cartRemoveButtons.forEach((cartRemoveButton)=>{
    cartRemoveButton.addEventListener('click',()=>{
        let currentCartItemCount = getSpecificCartItemCount(cartRemoveButton.id)
        console.log(currentCartItemCount)
        let newNumberOfCartItems = 0
        newNumberOfCartItems= currentCartItemCount -=1
        console.log(newNumberOfCartItems)
        

        fetch(urll,{
            method:'PUT',
            'headers': {
                'Content-Type':'application/json',
                'X-CSRFToken':'{{csrf_token}}'
            },
            body:JSON.stringify(
                {
                    "quantity":newNumberOfCartItems
                }
            )
        }).then((response)=>{
            return response.json
        }).then(()=>{
            window.location = "/updatecart/"
        })
    })
})


// end add and remove items from cart using increment and decrement signs