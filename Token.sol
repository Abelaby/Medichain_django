// SPDX-License-Identifier: MIT
pragma solidity  ^0.8.0;
contract Token {
    event NewToken(string signature, string receiver, string token);
    struct TokenData {
        string signature;
        string receiver;
        string token;
    }
    TokenData[] public tokens;
    mapping(uint => address) public tokenToOwner;
    mapping(address => string) public signToToken;

    function saveToken(string memory signature, string memory receiver, string memory token) public payable returns (bool) {
        uint id = tokens.length;
        tokens.push(TokenData(signature, receiver, token));
        tokenToOwner[id] = msg.sender;
        signToToken[msg.sender] = signature;
        emit NewToken(signature, receiver, token);
        return true;
    }

    function getToken(string memory signature, string memory receiver) public view returns (string memory) {
        for (uint i = 0; i < tokens.length; i++) {
            TokenData storage myToken = tokens[i];
            if (keccak256(bytes(signature)) == keccak256(bytes(myToken.signature)) && keccak256(bytes(receiver)) == keccak256(bytes(myToken.receiver))) {
                return myToken.token;
            }
        }
        return "wrong input or no record";
    }
}
