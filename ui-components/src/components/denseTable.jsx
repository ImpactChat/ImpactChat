import React, { useState } from 'react';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import TablePagination from '@material-ui/core/TablePagination';
import Paper from '@material-ui/core/Paper';
import LinearProgress from '@material-ui/core/LinearProgress';
import Box from '@material-ui/core/Box';
import PropTypes from 'prop-types';

class DenseTable extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            loaded: false,
            data: {},
            page: 0,
            rowsPerPage: 5,
            type: props.type
        };
        this.getData = this.getData.bind(this);
    }

    componentDidMount() {
        this.getData();
    }

    componentDidUpdate() {
        if (this.props.test !== undefined)
        {
            if (this.props.test['api-name'] !== this.state.type)
            {
                this.setState({type: this.props.test['api-name']})
                this.getData();
            }
        }
    }

    getData(page) {
        this.setState({
            isLoaded: false,
        })
        const source = this.props.source;
        const full_source = window.location.protocol + "//" + window.location.host + source;

        const get_params = {
            "page": page + 1 || (this.state.page + 1).toString(),
            "max": this.props.rowsPerPage || this.state.rowsPerPage,
            "type": this.props.type
        }

        var url = new URL(full_source),
            params = get_params
        Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))

        fetch(url, {
            method: 'GET',
        })
            .then(res => res.json())
            .then(data => (
                this.setState({
                    isLoaded: true,
                    data: data
                })
            ))
    }

    render() {
        if (!this.state.isLoaded) {
            return <LinearProgress />

        }
        const headers = this.props.headers;
        const rows = this.props.data;
        
        const handleChangePage = (event, newPage) => {
            this.setState({page: newPage})
            this.getData(newPage)
        };        

        console.log(this.props.rowsPerPage)


        return (
            <TableContainer component={Paper}>
                <Table size="small" aria-label="a dense table">
                    <TableHead>
                        <TableRow>
                            {
                                headers.map((val, i) => {
                                    return (
                                        <TableCell key={val.actual}>
                                            <Box fontWeight={900} align={i === 0 ? "left" : "right"} >
                                                {val.display}
                                            </Box>
                                        </TableCell>
                                    );
                                })
                            }
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {this.state.data.items.map((data) => (
                            <TableRow key={data.pk}>
                                {
                                    this.props.headers.map((val, i) => (
                                        <TableCell key={val.actual} align={i === 0 ? "left" : "right"} component={i === 0 ? "th" : "td"} scope={i === 0 ? "row" : undefined}>
                                            {data[val.actual]}
                                        </TableCell>
                                    ))
                                }
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
                <TablePagination
                    rowsPerPageOptions={[this.props.rowsPerPage || this.state.rowsPerPage]}
                    component="div"
                    count={this.state.data.count}
                    rowsPerPage={this.props.rowsPerPage || this.state.rowsPerPage}
                    page={this.state.page}
                    onChangePage={handleChangePage}
                />
            </TableContainer>
        );
    }
}

DenseTable.propTypes = {
    headers: PropTypes.arrayOf(PropTypes.object).isRequired,
    source: PropTypes.string.isRequired,
    type: PropTypes.string.isRequired,
    rowsPerPage: PropTypes.number
};
// export default withStyles(styles)(DenseTable);
export default DenseTable;