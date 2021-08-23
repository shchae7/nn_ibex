SRCS=$(filter-out vibes.cpp, $(wildcard *.cpp))
BINS=$(SRCS:.cpp=)

CXXFLAGS := $(shell pkg-config --cflags ibex) 
LIBS	 := $(shell pkg-config --libs  ibex)

ifeq ($(DEBUG), yes)
CXXFLAGS := $(CXXFLAGS) -O0 -g -pg -Wall 
else
CXXFLAGS := $(CXXFLAGS) -O3 -DNDEBUG 
endif

CXXFLAGS := $(CXXFLAGS) -std=c++11 -DIBEX_BENCHS_DIR=\"${ROOT_DIR}../benchs/solver\" -U__STRICT_ANSI__


all: $(BINS)

% :	%.cpp
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -o $@ $< $(LIBS)

clean:
	rm -f $(BINS) 
	
#plugins/optim/examples/doc-contractor.cpp
