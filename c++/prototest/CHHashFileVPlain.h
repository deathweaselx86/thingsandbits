/*
Extremely truncated piece of the Cryptohaze Multiforcer & Wordyforcer - low performance GPU password cracking
Copyright (C) 2011  Bitweasil (http://www.cryptohaze.com/)

Hacked to hell and back version not-so-copyright Cybergray.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
*/

/**
 * @section DESCRIPTION
 * CHHashFileVPlain is an implementation of the CHHashFileV class for 
 * plain (unsalted/simple) hash types such as MD5, NTLM, SHA1, etc.
 * 
 * This class deals with files that have one hash per line, in ASCII-hex 
 * notation, newline separated.  It is provided the length of the hash and 
 * will ignore hashes that are not the correct length in the file.
 */



#ifndef _CHHASHFILEVPLAIN_H
#define _CHHASHFILEVPLAIN_H

#include "CHHashFileVPlain.pb.h"

#include <iostream>
#include <ostream>
#include <iomanip>
#include <stdint.h>
#include <cstdlib>
#include <fstream>

class CHHashFileVPlain {
    private:
    /**
     * A structure to contain data on each hash found.
     * 
     * This structure contains the various fields related to each hash.
     */
    typedef struct HashPlain {
        
        std::vector<uint8_t> hash; /**< Hash in file order */
        std::vector<uint8_t> password; /**< Password related to the hash, or null */
        char passwordPrinted; /**< True if the password has been printed to screen */
        char passwordFound; /**< True if the password is found. */
        char passwordOutputToFile; /**< True if the password has been placed in the output file. */

    } HashPlain;

    
    /**
     * A vector of all loaded hashes.
     * 
     * This is the main store of hashes.  It contains an entry for each line of
     * the hashfile loaded.
     */
    std::vector<HashPlain> Hashes;
    
    /**
     * The current hash length in bytes.
     */
    uint32_t HashLengthBytes;
    
   
    /*
     *
     * Prints the contents of one uint8_t for the purposes of debugging. 
     *
     */
    void printVector(std::vector<uint8_t> vec);

    public:
    /*
     * Makes a bunch of random HashPlains and put them into Hashes.
     * Each HashPlain has hash the same length as HashLengthBytes, null password,
     * and all char fields set to '0'
     * 
     */
    void makeRandom();
   
   /*
    *
    * Prints contents of this CHHashFileVPlain in a debug format to stdout.
    *
    */
    void printContents();


    /**
     * Default constructor for CHHashFileVPlain.
     * 
     * Clears variables as needed.  All non-stl variables should be cleared.
     * 
     * @param newHashLengthBytes The length of the target hash type, in bytes.
     */
    CHHashFileVPlain(int newHashLengthBytes){
    	this->Hashes.clear();
    	this->HashLengthBytes = newHashLengthBytes;
    }

    /*
     * Deserializes a remote system's CHHashFileVPlain data from
     * a Google Protocol Buffer Message object and put it into this CHHashFileVPlain.
     * This CHHashFileVPlain will be reset first.
     *
     * @param remoteData A reference to the Protocol Buffer Message object 
     *
     * What happens if that object is invalid in some way? That's what this code and the 
     * Protobuf documentation is for.
     */
    virtual void ImportHashListFromRemoteSystem(::google::protobuf::Message & remoteData);
 
    /*
     * Serializes data from this CHHashFileVPlain into a Google Protocol Buffer
     * Message object for transmission to a remote system.
     *
     * @param exportData A reference to the Protocol Buffer Message object
     *
     * What happens if that object is invalid in some way? That's what this code and the 
     * Protobuf documentation is for.
     */
    virtual void ExportHashListToRemoteSystem(::google::protobuf:: Message &exportData);

    /**
     * Returns the current hash length in bytes.
     * 
     * @return Hash length in bytes.
     */
    virtual uint32_t GetHashLengthBytes() {
        return this->HashLengthBytes;
    }
    
};


#endif

    
