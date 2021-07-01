import React from "react";
import STYLES from "./Nav.module.scss";
import DH_LOGO from "../../images/dh_logo.svg";

const Nav = () => {

    return (
        <nav className="navbar navbar-light bg-light">
            <a className={`navbar-brand ${STYLES.linkHome}`} href="/">Gender Analysis Toolkit</a>
            <ul className="navbar-nav mr-auto">
                <li className="nav-item">
                    <a className="nav-link" href="/documents">
                        Documents
                    </a>
                </li>
            </ul>
            <a className={STYLES.linkLab} href="https://digitalhumanities.mit.edu/" target="_blank" rel="noreferrer">
               <img className={STYLES.imageLab} src={DH_LOGO} />
            </a>
        </nav>
    );
};

export default Nav;
