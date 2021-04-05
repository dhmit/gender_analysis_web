import React from 'react';
import * as PropTypes from 'prop-types';
import { Navbar, Footer } from '../UILibrary/components';

export class ExampleView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            responseId: null,
            responseText: null,
        };
    }

    async componentDidMount() {
        try {
            const apiURL = `/api/example/${this.props.exampleId}`;
            const data = await fetch(apiURL);
            const { name, id} = await data.json();
            this.setState({
                responseText: name,
                responseId: id,
            });
        } catch (e) {
            console.log(e);
        }
    }

    render() {
        return (
            <React.Fragment>
                <Navbar />
                <main className="main container-fluid">
                    <div className="col-12 py-3">
                        <h1>Title</h1>
                        <p>Content</p>
                        <p>Example URL param hydration: { this.props.exampleId }</p>
                        <p>Example API respones: { this.state.responseId }, { this.state.responseText }</p>
                    </div>
                </main>
                <Footer />
            </React.Fragment>
        );
    }
}

ExampleView.propTypes = {
    exampleId: PropTypes.number,
};
