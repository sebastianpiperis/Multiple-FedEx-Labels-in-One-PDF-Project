<?php



    function getPDF($zplFilePath) {
        
        
        // Read ZPL content from the constructed path
        $zpl = file_get_contents($zplFilePath);
        if (!$zpl) {
            die("Failed to read the ZPL file.");
        }
    
        $curl = curl_init();
        // adjust print density (8dpmm), label width (4 inches), label height (6 inches), and label index (0) as necessary
        curl_setopt($curl, CURLOPT_URL, "http://api.labelary.com/v1/printers/8dpmm/labels/4x7/0/");
        curl_setopt($curl, CURLOPT_POST, TRUE);
        curl_setopt($curl, CURLOPT_POSTFIELDS, $zpl);
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, TRUE);
        curl_setopt($curl, CURLOPT_HTTPHEADER, array("Accept: application/pdf")); // omit this line to get PNG images back
        $result = curl_exec($curl);
    
        if (curl_getinfo($curl, CURLINFO_HTTP_CODE) == 200) {
            // Extract the ID from the path to construct the PDF save path
            $id = basename($zplFilePath);
            $pdfSavePath = "PDF/{$id}/label2.pdf";
            
            // Ensure the directory exists
            if (!is_dir(dirname($pdfSavePath))) {
                mkdir(dirname($pdfSavePath), 0777, true);
            }
            
            $file = fopen($pdfSavePath, "w");
            fwrite($file, $result);
            fclose($file);
        } else {
            print_r("Error: $result");
        }
    
        curl_close($curl);
    }

    $zplFilePath = '794982482877'; // Adjust as necessary, ensure the ZPL file exists in this folder
    getPDF($zplFilePath);
    

?>

