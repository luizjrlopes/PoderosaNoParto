import styled from 'styled-components';

export const Container = styled.div`

align-items:center;


width: 100%;//1920px;
height: 100px;
background:#6D3E5D;
border-bottom: 10px solid #C79518;
display:flex;
position:relative;


`
export const LeftSide = styled.div`
width: 100%;//1920px;
height: 100px;
//zoom: 1.2;

display:flex;
align-items:center;

img{
  
margin-top:10px;
margin-left:10px;
width:486px;
height:80px;
    
    }
    

`
export const RightSide = styled.div`
width:100%;//960px;
height:100%;//905px;

align-items:center;

display:flex;


`

export const Menu = styled.div`

width:1920px;
height: 56px;
display:flex;
align-items: center;


.dividir::after{
    content:"|"; 
 color: #C79518;
margin:0 1px;
font-size:30px;
font-style:arial;
padding:1px;

};
a{
color:#6D3E5D;
font-weight: bold;
text-decoration:none;
margin: 0px 5px;
font-size:30px;
font-style:arial;

&:hover{
    
color: #C79518;
}

};





`


