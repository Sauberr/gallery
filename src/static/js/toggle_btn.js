        const toggleBtn = document.querySelector('.toggle_btn');
        const dropDownMenu = document.querySelector('.dropdown_menu');

        toggleBtn.onclick = function () {
        this.classList.toggle("change");
        dropDownMenu.classList.toggle('open');
    }