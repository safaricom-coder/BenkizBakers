const container = document.querySelector('.breadcrumb-option')
let title = document.querySelector('.title').innerHTML
container.innerHTML = ''
function updateContainer(pagename){
    text = `
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
