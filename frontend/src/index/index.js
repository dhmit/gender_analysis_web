import React from 'react';
import { Navbar, Footer } from '../UILibrary/components';

export class IndexView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
        };
    }

    render() {
        return (
            <React.Fragment>
                <Navbar />
                <main className="main container-fluid">
                    <div className="col-12 py-3">
                        <h1>Title</h1>
                        <p>Content</p>
                    </div>
                </main>
                <Footer />
            </React.Fragment>
        );
    }
}
export default IndexView;
