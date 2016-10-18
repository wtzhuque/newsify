package main

import (
  "fmt"
  "flag"
  "time"
  "net/http"
  "sync/atomic"
)

type SeqGenerator  struct {
    cluster_id int
    host_id int
    offset uint64
}

func NewSeqGenerator(cluster_id int, host_id int) *SeqGenerator {
    return &SeqGenerator{cluster_id, host_id, 0}
}

func (seq *SeqGenerator) generate() uint64 {
    var tmp_id = atomic.AddUint64(&seq.offset, uint64(1))
    var t = uint64(time.Now().UnixNano() / 1000)
    var id = ((t & 0x1FFFFFFFFFF) << 22) +
             ((uint64(seq.cluster_id) & 0x1F) << 17) +
             ((uint64(seq.host_id) & 0x1F) << 12) +
             (tmp_id & 0xFFF)
    return id
}

type Server struct {
    port int
    seq *SeqGenerator
}

func NewServer(port int, seq *SeqGenerator) *Server {
    return &Server{port, seq}
}

func (server *Server) start() {
    http.HandleFunc("/get", server.http_get)
    var addr = fmt.Sprintf(":%d", server.port)
    http.ListenAndServe(addr, nil)
}

func (server *Server) http_get(res_writer http.ResponseWriter, req *http.Request) {
    var id = server.seq.generate()
    fmt.Fprintf(res_writer, "%d", id)
}

func main() {
  var port = flag.Int("port", 8080, "Service Port")
  var cluster_id = flag.Int("cluster_id", 0, "Cluster ID")
  var host_id = flag.Int("host_id", 0, "Host ID")

  var seq = NewSeqGenerator(*cluster_id, *host_id)
  var server = NewServer(*port, seq)

  server.start()
}
