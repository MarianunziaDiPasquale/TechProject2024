
            <?php
            $db = new SQLite3('resources/orders_fattura.db');
            $invoice_number = '3';
            $result = $db->query("SELECT * FROM orders_fattura WHERE ID = '$invoice_number'");
            $invoice = $result->fetchArray(SQLITE3_ASSOC);
            ?>
            <!DOCTYPE html>
            <html>
            <head>
                <title>Invoice</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                    }
                    .container {
                        width: 80%;
                        margin: 0 auto;
                        padding: 20px;
                    }
                    .header, .section {
                        display: grid;
                        grid-template-columns: repeat(2, 1fr);
                        gap: 20px;
                        margin-bottom: 20px;
                    }
                    .header div, .section div {
                        padding: 10px;
                        border: 1px solid #ddd;
                    }
                    .header {
                        background-color: #f2f2f2;
                    }
                    h1, h2 {
                        grid-column: span 2;
                        text-align: center;
                    }
                    table {
                        width: 100%;
                        border-collapse: collapse;
                        margin-bottom: 20px;
                    }
                    th, td {
                        border: 1px solid black;
                        padding: 8px;
                        text-align: left;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <div>
                            <h1>INVOICE n°<?php echo $invoice['ID']; ?></h1>
                            <p>Date: <?php echo $invoice['date']; ?></p>
                        </div>
                        <div>
                            <h2>Goods destination</h2>
                            <p><?php echo $invoice['customer_name']; ?></p>
                            <p><?php echo $invoice['customer_address']; ?></p>
                            <p><?php echo $invoice['customer_phone']; ?></p>
                            <p><?php echo $invoice['customer_email']; ?></p>
                            <p>VAT: <?php echo $invoice['vat_number']; ?></p>
                            <p>Nation: <?php echo $invoice['nation']; ?></p>
                            <p>Time Zone: <?php echo $invoice['Time_zone']; ?></p>
                            <p>Skype Contact: <?php echo $invoice['SKYPE_contact']; ?></p>
                            <p>Language: <?php echo $invoice['Language']; ?></p>
                            <p>Client Type: <?php echo $invoice['Client_type']; ?></p>
                            <p>Comanda: <?php echo $invoice['Comanda']; ?></p>
                            <p>Date: <?php echo $invoice['Date_1']; ?></p>
                        </div>
                    </div>

                    <div class="section">
                        <div>
                            <h2>Bank Details</h2>
                            <p>IBAN: <?php echo $invoice['iban']; ?></p>
                            <p>Swift: <?php echo $invoice['swift']; ?></p>
                        </div>
                        <div>
                            <h2>Agent</h2>
                            <p><?php echo $invoice['agent_name']; ?></p>
                        </div>
                        <div>
                            <h2>Payment Condition</h2>
                            <p><?php echo $invoice['payment_condition']; ?></p>
                        </div>
                        <div>
                            <h2>Sender</h2>
                            <p><?php echo $invoice['sender_name']; ?></p>
                        </div>
                    </div>

                    <h2>Products</h2>
                    <table>
                        <tr>
                            <th>Article</th>
                            <th>Description</th>
                            <th>Code</th>
                            <th>Quantity</th>
                            <th>Price</th>
                            <th>Discount</th>
                            <th>Amount</th>
                        </tr>
                        <?php
                        $products_result = $db->query("SELECT * FROM orders_fattura WHERE ID = '$invoice_number'");
                        while ($product = $products_result->fetchArray(SQLITE3_ASSOC)) {
                            echo "<tr>
                                <td>" . $product['article'] . "</td>
                                <td>" . $product['product_description'] . "</td>
                                <td>" . $product['product_code'] . "</td>
                                <td>" . $product['product_quantity'] . "</td>
                                <td>" . $product['product_price'] . "</td>
                                <td>" . $product['product_discount'] . "</td>
                                <td>" . $product['product_amount'] . "</td>
                            </tr>";
                        }
                        ?>
                    </table>

                    <div class="section">
                        <div>
                            <h2>Total</h2>
                            <p>Total Quantity: <?php echo $invoice['total_quantity']; ?></p>
                            <p>Total Amount: <?php echo $invoice['total_amount_1']; ?></p>
                            <p>IVA Amount: <?php echo $invoice['iva_amount_1']; ?></p>
                            <p>Net Amount: <?php echo $invoice['Net_Amount']; ?></p>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            