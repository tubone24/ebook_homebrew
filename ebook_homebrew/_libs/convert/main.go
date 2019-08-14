package main

import (
	"C"
	"bytes"
	"github.com/jung-kurt/gofpdf"
	"path/filepath"
)

func convertPDF(path string, extension string) error {
	pdf := gofpdf.New("P", "mm", "A4", "")
	var pattern bytes.Buffer
	pattern.WriteString(path)
	pattern.WriteString("/*.")
	pattern.WriteString(extension)
	files, _ := filepath.Glob(pattern.String())
	for _, file := range files {
		pdf.AddPage()
		pdf.ImageOptions(file, 0, 0, 210, 297, false, gofpdf.ImageOptions{ImageType: extension, ReadDpi: true}, 0, "")
	}
	var resultName bytes.Buffer
	resultName.WriteString(path)
	resultName.WriteString("/result.pdf")
	err := pdf.OutputFileAndClose(resultName.String())
	if err != nil {
		return err
	}
	return nil
}

func main() {}
