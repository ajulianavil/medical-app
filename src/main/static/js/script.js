 //ejecutar funcion en el evento click

 document.getElementById("boton_open").addEventListener("click",open_close_menu)
 //declaramos las variables

 var menu_side=document.getElementById("menu_side");
 var boton_open=document.getElementById("boton_open");
 var body=document.getElementById("body");

  //evento para mostrar y ocultar el menú
   function open_close_menu(){
     body.classList.toggle("body_move");
     menu_side.classList.toggle("menu__side_move");
   }

   //si el ancho de la pagina es menos a 760px, ocultará el menú al recargar  la pagina

   if (window.innerWidth < 760){
    body.classList.add("body_move");
    menu_side.classList.add("menu__side_move");
   }

   //haciendo el menú responsive
   window.addEventListener("resize",function(){

    if(window.innerWidth>760){

      body.classList.remove("body_move");
      menu_side.classList.remove("menu__side_move");
    }

    if(window.innerWidth<760){

      body.classList.add("body_move");
      menu_side.classList.add("menu__side_move");
    }
   });

