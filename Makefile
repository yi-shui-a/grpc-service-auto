
# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
HOST_SYSTEM = $(shell uname | cut -f 1 -d_)
SYSTEM ?= $(HOST_SYSTEM)
CXX = g++
CPPFLAGS += `pkg-config --cflags protobuf grpc`
CXXFLAGS += -std=c++11
ifeq ($(SYSTEM),Darwin) 
LDFLAGS += -L/usr/local/lib `pkg-config --libs protobuf grpc++ grpc`\
        	-lgrpc++_reflection\
        	-ldl -lpthread\

INCLUDES = -I ./atom_inc
INCLUDES += -I ./rpc_server_inc
INCLUDES += -I ./rpc_client_inc
INCLUDES += -I /usr/local/include/nlohmann
else
LDFLAGS += -L/usr/local/lib `pkg-config --libs protobuf grpc++ grpc`\
        	-Wl,--no-as-needed -lgrpc++_reflection -Wl,--as-needed\
        	-ldl -lpthread\

#           -ldl -lprotobuf -lpthread
INCLUDES = -I ./atom_inc
INCLUDES += -I ./rpc_server_inc
INCLUDES += -I ./rpc_client_inc
INCLUDES += -I /usr/local/include/nlohmann


# -I /usr/local/include
endif

PROTOC = protoc
GRPC_CPP_PLUGIN = grpc_cpp_plugin
GRPC_CPP_PLUGIN_PATH ?= `which $(GRPC_CPP_PLUGIN)`

SRC_PATH = ./src
OBJS_PATH = ./objs
PROTOS_PATH = ./protos
BIN_PATH = ./bin

ATOM_SERVER_SRC = ./atom_src
ATOM_SERVER_INC = ./atom_inc
GRPC_SERVER_INC = ./rpc_server_inc
GRPC_CLIENT_INC = ./rpc_client_inc

vpath %.cpp $(SRC_PATH) 
vpath %.proto $(PROTOS_PATH)

SERVER_DEPEND_ELEMENTS = ?= default_server_depend_elements
CLIENT_DEPEND_ELEMENTS = ?= default_client_depend_elements
ASYNC_SERVER_DEPEND_ELEMENTS = ?= default_async_server_depend_elements

# SERVER = ${FIRST_ELEMENT}
# CLIENT = $(SECOND_ELEMENT) # Released version
# CLIENT_TEST = client   # test version
SERVER = ServerMain
CLIENT = ClientMain

SERVER = ServerMain
ASYNC_SERVER = AsyncServerMain

# all: system-check $(BIN_PATH)/$(SERVER) $(BIN_PATH)/$(CLIENT)
# all: system-check $(BIN_PATH)/$(SERVER) $(BIN_PATH)/$(CLIENT_TEST)
all: system-check $(BIN_PATH)/$(SERVER) $(BIN_PATH)/$(CLIENT) $(BIN_PATH)/$(ASYNC_SERVER)
# system-check:
	@echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>================================"
	@echo "System: $(SYSTEM)"
	@echo "CXX: $(CXX)"
	@echo "CXXFLAGS: $(CXXFLAGS)"
	@echo "LDFLAGS: $(LDFLAGS)"
	@echo "GRPC_CPP_PLUGIN_PATH: $(GRPC_CPP_PLUGIN_PATH)"
	@echo "PROTOC: $(PROTOC)"
	@echo "SRC_PATH: $(SRC_PATH)"
	@echo "OBJS_PATH: $(OBJS_PATH)"
	@echo "PROTOS_PATH: $(PROTOS_PATH)"
	@echo "BIN_PATH: $(BIN_PATH)"
	@echo "ATOM_SERVER_SRC: $(ATOM_SERVER_SRC)"
	@echo "ATOM_SERVER_INC: $(ATOM_SERVER_INC)"
	@echo "GRPC_SERVER_INC: $(GRPC_SERVER_INC)"
	@echo "GRPC_CLIENT_INC: $(GRPC_CLIENT_INC)"
	@echo "SERVER_DEPEND_ELEMENTS: $(SERVER_DEPEND_ELEMENTS)"
	@echo "CLIENT_DEPEND_ELEMENTS: $(CLIENT_DEPEND_ELEMENTS)"
	@echo "ASYNC_SERVER_DEPEND_ELEMENTS: $(ASYNC_SERVER_DEPEND_ELEMENTS)"

	@for i in  $(SERVER_DEPEND_ELEMENTS); do \
		echo $$i; \
	done
	@echo "-----------------------------------------------------------------------"
	@for i in  $(CLIENT_DEPEND_ELEMENTS); do \
		echo $$i; \
	done
	@echo "-----------------------------------------------------------------------"
	@for i in  $(ASYNC_SERVER_DEPEND_ELEMENTS); do \
		echo $$i; \
	done
	@echo "==================================<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"



$(BIN_PATH)/$(SERVER): $(SERVER_DEPEND_ELEMENTS)
	@echo ">>>>[INFO] Linking $(SERVER)..."
	$(CXX) $^ $(LDFLAGS) -o $@
$(BIN_PATH)/$(CLIENT): $(CLIENT_DEPEND_ELEMENTS)
	@echo ">>>>[INFO] Linking $(CLIENT)..."
	$(CXX) $^ $(LDFLAGS) -o $@

$(BIN_PATH)/$(ASYNC_SERVER): $(ASYNC_SERVER_DEPEND_ELEMENTS)
	@echo ">>>>[INFO] Linking $(ASYNC_SERVER)..."
	$(CXX) $^ $(LDFLAGS) -o $@



$(OBJS_PATH)/%.o: $(SRC_PATH)/%.cpp
	@echo '>>>>[INFO] Compiling $<...'
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

$(OBJS_PATH)/%.o: $(ATOM_SERVER_SRC)/%.cpp
	@echo '>>>>[INFO] Compiling $<...'
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@


$(OBJS_PATH)/%.pb.o: $(PROTOS_PATH)/%.pb.cc
	@echo '>>>>[INFO] Compiling $<...'
	$(CXX) $(CXXFLAGS) -c $< -o $@
$(OBJS_PATH)/%.grpc.pb.o: $(PROTOS_PATH)/%.grpc.pb.cc
	@echo '>>>>[INFO] Compiling $<...'
	$(CXX) $(CXXFLAGS) -c $< -o $@

.PRECIOUS: %.grpc.pb.cc
%.grpc.pb.cc:  %.proto
	$(PROTOC) -I$(PROTOS_PATH) --grpc_out=$(PROTOS_PATH)  --plugin=protoc-gen-grpc=$(GRPC_CPP_PLUGIN_PATH) $<
.PRECIOUS: %.pb.cc
%.pb.cc: %.proto
	$(PROTOC) -I$(PROTOS_PATH) --cpp_out=$(PROTOS_PATH)  $<

clean:
	@echo ">>>>[INFO] Cleaning up..."
	rm -f $(OBJS_PATH)/*.o $(OBJS_PATH)/*.o $(PROTOS_PATH)/*.pb.cc $(PROTOS_PATH)/*.pb.h $(PROTOS_PATH)/*.proto $(BIN_PATH)/*
	rm -f $(ATOM_SERVER_INC)/*h
	@echo ">>>>[INFO] Cleanup finished."



PROTOC_CMD = which $(PROTOC)
PROTOC_CHECK_CMD = $(PROTOC) --version | grep -q libprotoc.3
PLUGIN_CHECK_CMD = which $(GRPC_CPP_PLUGIN)
HAS_PROTOC = $(shell $(PROTOC_CMD) > /dev/null && echo true || echo false)
ifeq ($(HAS_PROTOC),true)
HAS_VALID_PROTOC = $(shell $(PROTOC_CHECK_CMD) 2> /dev/null && echo true || echo false)
endif
HAS_PLUGIN = $(shell $(PLUGIN_CHECK_CMD) > /dev/null && echo true || echo false)

SYSTEM_OK = false
ifeq ($(HAS_VALID_PROTOC),true)
ifeq ($(HAS_PLUGIN),true)
SYSTEM_OK = true
endif
endif

system-check:
ifneq ($(HAS_VALID_PROTOC),true)
	@echo " DEPENDENCY ERROR"
	@echo
	@echo "You don't have protoc 3.0.0 installed in your path."
	@echo "Please install Google protocol buffers 3.0.0 and its compiler."
	@echo "You can find it here:"
	@echo
	@echo "   https://github.com/google/protobuf/releases/tag/v3.0.0"
	@echo
	@echo "Here is what I get when trying to evaluate your version of protoc:"
	@echo
	-$(PROTOC) --version
	@echo
	@echo
endif
ifneq ($(HAS_PLUGIN),true)
	@echo " DEPENDENCY ERROR"
	@echo
	@echo "You don't have the grpc c++ protobuf plugin installed in your path."
	@echo "Please install grpc. You can find it here:"
	@echo
	@echo "   https://github.com/grpc/grpc"
	@echo
	@echo "Here is what I get when trying to detect if you have the plugin:"
	@echo
	-which $(GRPC_CPP_PLUGIN)
	@echo
	@echo
endif
ifneq ($(SYSTEM_OK),true)
	@false
endif
