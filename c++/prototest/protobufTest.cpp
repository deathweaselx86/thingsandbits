/*
 * This is some hacked together code used to check out Google's Protocol Buffers for use
 * in cryptohaze.
 *
 * Check out cryptohaze, a set of password security auditing tools. Find it here:
 * http://cryptohaze.com 
 * More info in CHHashFileVPlain.h.
 *
 * Also out the Protocol Buffers, they are awesome, but not so awesome that you don't have to think a little.
 * http://code.google.com/p/protobuf/
 * 
 *How to compile this: 
 * Make protobuf generated code with this line: 
 * protoc CHHashFileVPlain.proto --cpp_out=.
 *
 * Make the rest of it with this line:
 * g++ protobufTest.cpp CHHashFileVPlain.pb.cc CHHashFileVPlain.cpp -I/usr/local/include/google/protobuf -lprotobuf -o test
 * 
 * */


#include "CHHashFileVPlain.h"

int main()
{
	//construct sample HashPlains
	std::srand(std::time(NULL));
	::MFNHashFilePlainProtobuf protobuf;
	int vectorLength = std::rand()%10+1;
	CHHashFileVPlain test(vectorLength), test2(vectorLength);
	std::fstream outputFile("test.txt", std::fstream::out | std::fstream::binary);

	test.makeRandom();	
	std::cout<<"Contents before serialization."<<std::endl;
	// Output contents of CHHashFileVPlain test
	test.printContents();
	::google::protobuf::Message & messageRef = dynamic_cast< ::google::protobuf::Message & >(protobuf);
	test.ExportHashListToRemoteSystem(messageRef);
	protobuf.SerializeToOstream(&outputFile);
	outputFile.close();
	outputFile.open("test.txt", std::fstream::in|std::fstream::binary);
	
	::MFNHashFilePlainProtobuf protobuf2;
	protobuf2.ParseFromIstream(&outputFile);
	outputFile.close();
	::google::protobuf::Message & messageRef2 = dynamic_cast< ::google::protobuf::Message & >(protobuf2);
	test2.ImportHashListFromRemoteSystem(messageRef2);
	std::cout<<"Contents after serialization"<<std::endl;
	test2.printContents();

	return 0;}
