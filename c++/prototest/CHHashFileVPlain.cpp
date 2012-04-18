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

#include "CHHashFileVPlain.h"

#define HEX( x ) std::setw(2) << std::setfill('0') << std::hex << (int)( x )



 void CHHashFileVPlain::printVector(std::vector<uint8_t> vec)
{
		std::vector<uint8_t>::iterator i;
		for(i = vec.begin(); i < vec.end(); i++)
			std::cout<<" "<<*i;
		std::cout<<std::endl;
}	


 void CHHashFileVPlain::printContents(){
 		std::vector<HashPlain>::iterator i;
 		int j = 0;
 		for (i=Hashes.begin(); i < Hashes.end(); i++)
 		{
 			std::cout<<"--------------"<<std::endl;
 			std::cout<<"	hash:";
 			printVector(i->hash);
 			std::cout<<"	password:";
 			printVector(i->password);
 			std::cout<<"	passwordPrinted: "<<i->passwordPrinted;
 			std::cout<<"	passwordFound: "<<i->passwordFound;
 			std::cout<<"	passwordOutputToFile: "<<i->passwordOutputToFile;
 			std::cout<<std::endl;
 			j++;
 		}
 	}
 
void CHHashFileVPlain::makeRandom(){
	std::vector<uint8_t> vec;
	int vectorLength = this->HashLengthBytes;
	for(int j=0;j<std::rand()%10+1;j++)
	        {
	                HashPlain sample;
	                for(uint8_t i=48; i < 48+vectorLength; i++)
	                        vec.push_back(std::rand() % 10 + i);
	                sample.hash = vec;
	                vec.clear();
	                for(uint8_t k=65; k < 65+vectorLength; k++)
	                        vec.push_back(std::rand() % 10 + k);
	                sample.password = vec;
	                vec.clear();
	                sample.passwordPrinted = '0';
	                sample.passwordFound = '1';
	                sample.passwordOutputToFile = '0';

	                Hashes.push_back(sample);
	        }

}

void CHHashFileVPlain::ImportHashListFromRemoteSystem(::google::protobuf::Message& remoteData) {
    // I hope your CHHashFileVPlain was empty.
    // For cleanliness, I will clean this now.
    Hashes.clear();
    HashLengthBytes = 0;

    //Cast Message object to MFNHashFileVPlainProtobuf and set up objects needed to retrieve
    //protobuf 

    ::MFNHashFilePlainProtobuf& protobuf = dynamic_cast< ::MFNHashFilePlainProtobuf& >(remoteData);
    // I am not sure what the performance hit is around instantiating the object everytime we have
    // unpack data. We should probably just provide a static MFNHashFifePlainProtobuf, etc object with this class.
    
    // We need this mess to access the fields we want.
    const ::google::protobuf::Descriptor * protobufDescriptor = protobuf.GetDescriptor();
    const ::google::protobuf::FieldDescriptor * hashFieldDescriptor = protobufDescriptor->FindFieldByName("hash_value");
    const ::google::protobuf::FieldDescriptor * lengthFieldDescriptor = protobufDescriptor->FindFieldByName("hash_length_bytes");
    
    // Reflection object is used to access values in the fields.
    const ::google::protobuf::Reflection * protobufReflection = protobuf.GetReflection();
    
    // Load hashes first.
    HashLengthBytes = protobufReflection->GetUInt32(protobuf, lengthFieldDescriptor);
    int numberOfHashes = protobufReflection->FieldSize(protobuf, hashFieldDescriptor);
    for(int i=0;i<numberOfHashes;i++)
    {
    	
    	HashPlain newHashPlain;
    	std::string thisHash= protobufReflection->GetRepeatedString(protobuf, hashFieldDescriptor, i);
    	// There's also a GetRepeatedStringReference() method. Can we leverage that?
    	std::vector<uint8_t> newVector = std::vector<uint8_t>(thisHash.begin(), thisHash.end()); 
    	newHashPlain.hash = newVector;
    	newHashPlain.passwordPrinted = '0';
    	newHashPlain.passwordFound = '0';
    	newHashPlain.passwordOutputToFile = '0';
    	Hashes.push_back(newHashPlain);
    }
    

    //Need to finish this.


}


void CHHashFileVPlain::ExportHashListToRemoteSystem(::google::protobuf::Message& exportData) {

    std::vector<HashPlain>::iterator i,j;
    //Later: try, except around this.
    ::MFNHashFilePlainProtobuf & protobuf = dynamic_cast< ::MFNHashFilePlainProtobuf & >(exportData);

    protobuf.set_hash_length_bytes(this->HashLengthBytes);
    for (i = this->Hashes.begin(); i < this->Hashes.end(); i++)
    {
        std::string hashString = std::string(i->hash.begin(), i->hash.end());
        protobuf.add_hash_value(hashString);
    }
}



//#define UNIT_TEST 1

#if UNIT_TEST

int main() {
    
    std::cout<<"foo"<<std::endl;
    
    CHHashFileVPlain HashFile(16);
    
    HashFile.OpenHashFile("foobar");
    std::cout<<(int)HashFile.GetTotalHashCount();
}

#endif
