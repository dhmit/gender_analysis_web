import React from "react";
import STYLES from "./Nav.module.scss";

const Nav = () => {

    return (
        <nav className={STYLES.nav}>
            <a className={STYLES.linkHome} href="/">
                App Title
            </a>
            <a className={STYLES.linkLab} href="https://digitalhumanities.mit.edu/" target="_blank" rel="noreferrer">
                <img className={STYLES.imageLab} src="/static/img/dh_logo.svg" />
            </a>
        </nav>
    );
};

export default Nav;
