import FooterLink from "./footerLink/footerLink";
import classes from "./footer.module.css";


const Footer = () => {
    const links = [
        "/static/media/instagram.svg",
        "/static/media/youtube.svg",
        "/static/media/vk.svg",
        "/static/media/facebook.svg"
    ];

    return (
        <section className={classes.footer_section}>
            <div className={classes.container}>
                <div className={classes.footer}>

                    <div className={classes.footer__links}>
                        <ul className={classes.footer__links_ul}>
                            {
                                links.map(link => <FooterLink image={link} key={link} />)
                            }
                        </ul>
                    </div>	
                    <div className={classes.footer__authors}>
                        <div className={classes.footer__authors_author}>
                            <div className={classes.footer__authors_author_title} id={classes.makariy}>
                                Makariy Corp.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}
export default Footer; 
