package main

import (
	"context"
	"log"
	"net/http"

	"github.com/grafana/pyroscope-go"

	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
	"go.opentelemetry.io/otel/sdk/resource"
	sdktrace "go.opentelemetry.io/otel/sdk/trace"
	semconv "go.opentelemetry.io/otel/semconv/v1.21.0"
)

func initTracer() func(context.Context) error {
	exp, err := otlptracegrpc.New(
		context.Background(),
		otlptracegrpc.WithEndpoint("otel-collector:4317"),
		otlptracegrpc.WithInsecure(),
	)
	if err != nil {
		log.Fatal(err)
	}

	tp := sdktrace.NewTracerProvider(
		sdktrace.WithBatcher(exp),
		sdktrace.WithResource(
			resource.NewWithAttributes(
				semconv.SchemaURL,
				semconv.ServiceName("go-api"),
			),
		),
	)

	otel.SetTracerProvider(tp)
	return tp.Shutdown
}

func initProfiler() {
	_, err := pyroscope.Start(pyroscope.Config{
		ApplicationName: "go-api",
		ServerAddress:   "http://pyroscope:4040",
		Tags: map[string]string{
			"service_name": "go-api",
		},
	})
	if err != nil {
		log.Fatal(err)
	}
}

func main() {
	shutdown := initTracer()
	defer shutdown(context.Background())

	initProfiler()

	tracer := otel.Tracer("go-api")

	http.HandleFunc("/work", func(w http.ResponseWriter, r *http.Request) {
		_, span := tracer.Start(r.Context(), "cpu-work")
		defer span.End()

		sum := 0
		for i := 0; i < 1_000_000_00; i++ {
			sum += i
		}

		w.Write([]byte("ok"))
	})

	log.Println("listening on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
