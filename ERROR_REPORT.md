# AgroScan AI — Diagnostic Error & Exception Catalog
**Date:** November 2026  
**System:** AgroScan AI Hybrid Intelligence Engine  

---

## 1. Error Handling Philosophy

AgroScan AI avoids generic, unhelpful error screens. Every diagnostic failure, validation rejection, or unsupported scenario maps to an explicit status code, localized messages in English and Marathi, technical explanations, and clear agronomic action items.

---

## 2. Standard Diagnostic Error Codes & Status Mappings

| Status Code | HTTP Status | English Message | Marathi Message (`mr`) | Root Cause | Farmer Recommended Action |
|---|:---:|---|---|---|---|
| `VALID_LEAF` | 200 OK | Leaf image validated successfully. | पानाचा फोटो यशस्वीरित्या पडताळला गेला. | Verified botanical foliage with chlorophyll spectrum. | Proceed to automated multi-model diagnosis. |
| `NON_LEAF_SELFIE` | 400 Bad Request | No clear leaf was detected in this image. Please capture a well-lit, focused photograph of the affected plant leaf. | या प्रतिमेत स्पष्टपणे पान आढळले नाही. कृपया बाधित पानाचा पुरेशा प्रकाशात आणि स्पष्टपणे फोटो काढा. | High skin tone area ($> 12\%$) or face detected via Haar cascade. | Switch camera away from face; capture close-up of plant leaf. |
| `DOCUMENT_DETECTED` | 400 Bad Request | The uploaded image appears to be a document, screenshot, or white page. | ही प्रतिमा दस्तऐवज, स्क्रीनशॉट किंवा पांढरा कागद वाटत आहे. कृपया प्रत्यक्ष पानाचा फोटो काढा. | White background ratio $> 45\%$ with high rectilinear contrast. | Capture an actual outdoor plant leaf; do not photograph screens or printed papers. |
| `BUILDING_DETECTED` | 400 Bad Request | Building, room, vehicle, or geometric structural object detected. | इमारत, खोली, वाहन किंवा कृत्रिम वस्तू आढळली आहे. कृपया पिकाच्या पानाचा फोटो काढा. | High rectilinear grid gradient metric ($> 0.14$) with foliage $< 8\%$. | Point camera directly at the crop in the field or garden. |
| `SOIL_ONLY_IMAGE` | 400 Bad Request | Soil or bare ground detected without clear leaf evidence. | जमिनीत केवळ माती किंवा शेतजमीन आढळली आहे, पान स्पष्ट दिसत नाही. | Elevated brown spectrum with low vegetation index. | Focus camera on a single leaf blade rather than bare ground. |
| `FLOWER_WITHOUT_LEAF`| 400 Bad Request | Flower or fruit detected without visible leaf foliage. | केवळ फूल किंवा फळ आढळले आहे. अचूक रोग निदानासाठी बाधित पानाचा फोटो आवश्यक आहे. | High floral petal chromaticity with green foliage $< 8\%$. | Move camera to include the supporting leaf foliage. |
| `INSUFFICIENT_IMAGE_QUALITY` | 400 Bad Request | The image is not clear enough for disease analysis. Please capture a well-lit, focused photograph of the affected plant leaf. | रोगाचे अचूक निदान करण्यासाठी फोटो पुरेसा स्पष्ट नाही. कृपया पानाचा स्पष्ट, स्थिर व चांगल्या प्रकाशातील फोटो काढा. | Laplacian variance $< 8.0$ (blurry) or extreme exposure ($< 15$ or $> 245$). | Hold camera steady, ensure good natural lighting, and tap screen to focus. |
| `UNSUPPORTED_CROP` | 200 OK (Honest) | AgroScan AI identified this specimen, but dedicated disease diagnostic models are not yet calibrated for this crop. | AgroScan AI ने या वनस्पतीची ओळख पटवली आहे, परंतु या विशिष्ट पिकासाठी रोग निदान मॉडेल्स अद्याप कॅलिब्रेट केलेले नाहीत. | Recognized crop (e.g. Tea, Coffee, Rubber) without calibrated local weights. | Review general cultivation guidelines and consult local Krishi Vigyan Kendra (KVK). |
| `UNCERTAIN` | 200 OK (Honest) | Diagnostic models produced conflicting assessments. Physical agronomic inspection is recommended. | मॉडेल्समध्ये परस्परविरोधी मते आढळली आहेत. प्रत्यक्ष कृषी अधिकाऱ्यांकडून पाहणी करून घेणे फायदेशीर ठरेल. | Calibrated confidence $< 0.50$ or conflicting model votes. | Retake photograph in diffused daylight focusing on lesion edges. |
| `PROVIDER_UNAVAILABLE`| 503 Service Unavailable | Disease detection services are temporarily unavailable. Please retry in a few moments. | रोग निदान सेवा तात्पुरती अनुपलब्ध आहे. कृपया काही क्षणांनंतर पुन्हा प्रयत्न करा. | All local models and external cloud adapters timed out or failed. | Check local network and system resources, then tap Retry. |
| `EMPTY_OR_OVERSIZED` | 400 Bad Request | Image file is empty or exceeds the limit of 10MB. | फोटो फाइल रिकामी आहे किंवा कमाल १० MB आकारापेक्षा जास्त आहे. | Byte length is 0 or $> 10$ MB. | Compress image or capture standard JPEG/WebP photo. |
| `FORBIDDEN_RECORD` | 403 Forbidden | You do not have permission to delete or modify this scan record. | तुम्हाला हा स्कॅन रेकॉर्ड हटवण्याची किंवा बदलण्याची परवानगी नाही. | Requesting user ID does not match scan owner ID. | Log into the correct farmer account. |
