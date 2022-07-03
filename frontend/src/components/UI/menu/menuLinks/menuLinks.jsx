import MenuLink from "./menuLink/menuLink";

import classes from "./menuLinks.module.css";


const MenuLinks = () => {

    const links = [
        {
            title: "Top",
            href: "#"
        },
        {
            title: "Actors",
            href: "#"
        },
        {     
            title: "Help",
            href: "#",
        }
    ]


    return (
        <div className={classes.menu__list}>
            <ul className={classes.menu__list_ul}>
                {
                    links.map(link => 
                        <MenuLink 
                            key={link.title} 
                            title={link.title}
                            href={link.href}
                        />
                    )
                }
            </ul>
        </div>
    );
}

export default MenuLinks;
