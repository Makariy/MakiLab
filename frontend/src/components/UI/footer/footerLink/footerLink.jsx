import classes from "./footerLink.module.css"


const FooterLink = ({image}) => {
    return (
        <li className={classes.links_li}>
            <a href="#" className={classes.link}>
                <img src={image} alt="" className={classes.link_img}/>
            </a>
        </li>
    );
}
export default FooterLink;
