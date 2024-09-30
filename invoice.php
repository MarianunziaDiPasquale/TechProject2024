
            <?php
            $servername = "localhost";
            $username = "your_username";
            $password = "your_password";
            $dbname = "your_database";

            $conn = new mysqli($servername, $username, $password, $dbname);

            if ($conn->connect_error) {
                die("Connection failed: " . $conn->connect_error);
            }

            $invoice_number = '1';

            $sql = "SELECT * FROM orders WHERE id = '$invoice_number'";
            $result = $conn->query($sql);

            if ($result->num_rows > 0) {
                $invoice = $result->fetch_assoc();
                ?>

                <!DOCTYPE html>
                <html>
                <head>
                    <title>Invoice</title>
                    <style>
                        /* Add your CSS styling here */
                    </style>
                </head>
                <body>
                    <h1>INVOICE n°<?php echo $invoice['id']; ?> Date: <?php echo $invoice['data']; ?></h1>
                    <h2>Goods destination</h2>
                    <p><?php echo $invoice['cliente']; ?></p>
                    <p><?php echo $invoice['indirizzo']; ?></p>
                    <p><?php echo $invoice['telefono']; ?></p>
                    <p><?php echo $invoice['email']; ?></p>
                    <p>VAT: <?php echo $invoice['vat_number']; ?></p>
                    <p>Nation: <?php echo $invoice['nation']; ?></p>
                    <p>Time Zone: <?php echo $invoice['Time_zone']; ?></p>
                    <p>Skype Contact: <?php echo $invoice['SKYPE_contact']; ?></p>
                    <p>Language: <?php echo $invoice['Language']; ?></p>
                    <p>Client Type: <?php echo $invoice['Client type']; ?></p>
                    <p>Comanda: <?php echo $invoice['Comanda']; ?></p>
                    <p>Date: <?php echo $invoice['Date_1']; ?></p>

                    <h2>Bank Details</h2>
                    <p>IBAN: <?php echo $invoice['iban']; ?></p>
                    <p>Swift: <?php echo $invoice['swift']; ?></p>

                    <h2>Agent</h2>
                    <p><?php echo $invoice['agent_name']; ?></p>

                    <h2>Payment Condition</h2>
                    <p><?php echo $invoice['payment_condition']; ?></p>

                    <h2>Sender</h2>
                    <p><?php echo $invoice['sender_name']; ?></p>

                    <h2>Products</h2>
                    <table border="1">
                        <tr>
                            <th>Code</th>
                            <th>Description</th>
                            <th>Quantity</th>
                            <th>Price</th>
                            <th>Discount</th>
                            <th>Amount</th>
                        </tr>

                        <?php
                        $result->data_seek(0);

                        while ($row = $result->fetch_assoc()) {
                            echo "<tr>
                                <td>" . $row['product_code'] . "</td>
                                <td>" . $row['product_description'] . "</td>
                                <td>" . $row['product_quantity'] . "</td>
                                <td>" . $row['product_price'] . "</td>
                                <td>" . $row['product_discount'] . "</td>
                                <td>" . $row['product_amount'] . "</td>
                            </tr>";
                        }
                        ?>

                    </table>

                    <h2>Total</h2>
                    <p>Total Quantity: <?php echo $invoice['total_quantity']; ?></p>
                    <p>Total Amount: <?php echo $invoice['total_amount']; ?></p>
                    <p>IVA Amount: <?php echo $invoice['iva_amount']; ?></p>
                    <p>Net Amount: <?php echo $invoice['net_amount']; ?></p>
                </body>
                </html>

                <?php
            } else {
                echo "No invoice found.";
            }

            $conn->close();
            ?>
            