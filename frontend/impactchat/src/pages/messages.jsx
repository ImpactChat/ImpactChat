import React from 'react';

import { withStyles } from "@material-ui/core/styles";

import MessageList from '../components/messageList';
import ChannelList from '../components/channelList';
import InputField from '../components/inputField';
import Settings from '../components/settings';
import { getCookie } from '../components/CSRFToken';


import Skeleton from '@material-ui/lab/Skeleton';
import InputAdornment from '@material-ui/core/InputAdornment';
import SendIcon from '@material-ui/icons/Send';
import IconButton from '@material-ui/core/IconButton';


import ReconnectingWebSocket from 'reconnecting-websocket';


const styles = theme => ({
  root: {
    flexGrow: 1,
  },
  content: {
    // marginTop: AppBar.height,
    paddingLeft: "0px"
  },
  title: {
    marginLeft: theme.spacing(2),
    flex: 1,
  },
  gridContainer: {
    display: 'grid',
    gridTemplateColumns: '0.5fr 2.1fr 0.4fr',
    gridTemplateRows: '0.0fr 3.3fr 0.2fr 0.1fr',
    gap: '1px 1px',
    gridTemplateAreas: `". . ." "Channels Messages Online" "Channels Input Online" "Channels . Online"`,
  },
  Online: { gridArea: 'Online',                         },
  Channels: { gridArea: 'Channels',                     },
  Messages: { gridArea: 'Messages', overflow: 'auto', maxHeight: '85vh' },
  Input: { gridArea: 'Input',                           },
  
});
// var pathname = window.location.pathname.sl ;
const roomName = window.location.pathname.split("/messages/")[1];
const chatSocket = new ReconnectingWebSocket(
  'ws://'
  + window.location.host
  + '/ws/chat/'
  + roomName
  + '/'
);


class MessageDisplay extends React.Component {

  scrollToBottom = () => {
    this.messagesEnd.scrollIntoView(false);
  };

  
  componentDidMount() {
    this.scrollToBottom();
  }
  
  componentDidUpdate() {
    this.scrollToBottom();
  }

  async getMessages() {
    const response = await fetch('/api/messages/get', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({channel: roomName}) // body data type must match "Content-Type" header
    });
    const res = await response.json();
    this.setState({messages: res.messages})
    this.setState({loading: false})
  }
  

  constructor(props)
  {
    super(props);
    this.state = {
      messages: ['a', 'b'],
      loading: true
    }
    this.getMessages = this.getMessages.bind(this);
    this.getMessages();
  }
  render() {
    const { classes } = this.props;

  

    document.body.style.overflow = "hidden";


    chatSocket.onopen = function(e) {
      console.log('Chat socket opened');
    };
    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        console.log("Received message from WS:", data);
        this.setState({messages: [...this.state.messages, data.new_message]})

    }.bind(this);

    chatSocket.onclose = function(e) {
        console.log('Chat socket closed');
    };



    return (
        <>
              <div className={classes.gridContainer}>
                  <div className={classes.Channels}>
                    <ChannelList />
                  </div>
                  <div className={classes.Messages}>
                    <MessageList loading={this.state.loading} messages={this.state.messages} />
                    <div style={{ float:"left", clear: "both" }}
                      ref={(el) => { this.messagesEnd = el; }}>
                  </div>
                  </div>
                  <div className={classes.Input}>
                    <MessageInput socket={chatSocket} />

                </div>
                <div className={classes.Online}>
                  <Settings toggle={this.props.toggle}/>
                  <Skeleton />
                </div>
              </div>
      </>
    );
  }
}

class MessageInput extends React.Component {
  handleInputChange = (e) => {
    this.setState({inputMessage: e.target.value})
  }

  handleInputSubmit = (e) => {
    e.preventDefault();
    if (this.state.inputMessage === "")
    {
      return
    }
    console.log("Sending:", this.state.inputMessage)
    this.props.socket.send(JSON.stringify({message: this.state.inputMessage, channel: roomName, type: 'chat.new'}));
    this.setState({inputMessage: ""})
  }

  constructor(props)
  {
    super(props);
    this.state = {
      inputMessage: ""
    }
    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleInputSubmit = this.handleInputSubmit.bind(this);
  }



  render() {
    return (
      <form onSubmit={this.handleInputSubmit}>
          <InputField
            style={{marginLeft: '10px', marginRight: '10px'}}
            variant="outlined"
            margin="normal"
            required
            fullWidth
            id="message"
            label="Message"
            name="message"
            autoComplete="off"
            value={this.state.inputMessage}
            onChange={this.handleInputChange}
            InputProps={{
              endAdornment: <InputAdornment position="end"> 
                <IconButton type={"submit"} onClick={this.handleInputSubmit}>
                    <SendIcon />
                </IconButton>
              </InputAdornment>,
            }}
        />
       
      </form>
  );
  }
}

export default withStyles(styles, { withTheme: true })(MessageDisplay);
