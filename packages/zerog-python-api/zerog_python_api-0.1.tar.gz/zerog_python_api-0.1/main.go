package main

import (
    "context"
    "encoding/json"
    "fmt"
    "io/ioutil"
    "os"
    // "math/big"

    "github.com/ethereum/go-ethereum/common"
    "github.com/ethereum/go-ethereum/common/hexutil"
    zg_common "github.com/0glabs/0g-storage-client/common"
    "github.com/0glabs/0g-storage-client/core"
    "github.com/0glabs/0g-storage-client/indexer"
    "github.com/0glabs/0g-storage-client/transfer"
    "github.com/0glabs/0g-storage-client/common/blockchain"
    "github.com/0glabs/0g-storage-client/contract"
    "github.com/sirupsen/logrus"
)

func main() {
    if len(os.Args) < 2 {
        fmt.Fprintf(os.Stderr, "Usage: ./cli_tool <command> [args...]\n")
        fmt.Fprintf(os.Stderr, "Commands: upload, download\n")
        os.Exit(1)
    }

    command := os.Args[1]

    switch command {
    case "upload":
        // Capture the Merkle root returned by the upload function
        err := upload(os.Args[2:])
        if err != nil {
            fmt.Fprintf(os.Stderr, "Upload failed: %v\n", err)
            os.Exit(1)
        }
    case "download":
        if err := download(os.Args[2:]); err != nil {
            fmt.Fprintf(os.Stderr, "Download failed: %v\n", err)
            os.Exit(1)
        }
    default:
        fmt.Fprintf(os.Stderr, "Unknown command: %s\n", command)
        os.Exit(1)
    }
}

func upload(args []string) error {
    if len(args) != 1 {
        return fmt.Errorf("Usage: ./cli_tool upload <json_args>")
    }

    var uploadArgs struct {
        File            string `json:"file"`
        Tags            string `json:"tags"`
        URL             string `json:"url"`
        Indexer         string `json:"indexer"`
        Contract        string `json:"contract"`
        Key             string `json:"key"`
        ExpectedReplica uint    `json:"expectedReplica"`
        FinalityRequired bool  `json:"finalityRequired"`
        SkipTx          bool   `json:"skipTx"`
        TaskSize        uint    `json:"taskSize"`
        // Fee             int64  `json:"fee"`
    }

    err := json.Unmarshal([]byte(args[0]), &uploadArgs)
    if err != nil {
        return fmt.Errorf("error parsing JSON arguments: %v", err)
    }

    ctx := context.Background()

    w3client := blockchain.MustNewWeb3("https://evmrpc-test-us.0g.ai/", uploadArgs.Key)
    defer w3client.Close()

    contractAddr := common.HexToAddress(uploadArgs.Contract)
    flow, err := contract.NewFlowContract(contractAddr, w3client)
    if err != nil {
        return fmt.Errorf("error creating flow contract: %v", err)
    }

    indexerClient, err := indexer.NewClient("https://rpc-storage-testnet-turbo.0g.ai", indexer.IndexerClientOption{
        LogOption: zg_common.LogOption{Logger: logrus.StandardLogger()},
    })
    if err != nil {
        return fmt.Errorf("error creating indexer client: %v", err)
    }

    fileContent, err := ioutil.ReadFile(uploadArgs.File)
    if err != nil {
        return fmt.Errorf("error reading file: %v", err)
    }

    opt := transfer.UploadOption{
        Tags:             hexutil.MustDecode(uploadArgs.Tags),
        FinalityRequired: uploadArgs.FinalityRequired,
        TaskSize:         uploadArgs.TaskSize,
        ExpectedReplica:  uploadArgs.ExpectedReplica,
        SkipTx:           uploadArgs.SkipTx,
        // Fee:              big.NewInt(uploadArgs.Fee),
    }

    dataArray, err := core.NewDataInMemory(fileContent)
    if err != nil {
        return fmt.Errorf("error creating data array: %v", err)
    }

    err = indexerClient.Upload(ctx, flow, dataArray, opt)
    if err != nil {
        return fmt.Errorf("error uploading file: %v", err)
    }

    // Add these lines before the return statement:

    // Calculate the Merkle tree and root
    tree, err := core.MerkleTree(dataArray)
    if err != nil {
        return fmt.Errorf("Failed to create data Merkle tree: %v", err)
    }

    // Extract the Merkle root
    merkleRoot := tree.Root().String()

    fmt.Printf(merkleRoot)
    return nil
}

func download(args []string) error {
    if len(args) != 2 {
        return fmt.Errorf("Usage: ./cli_tool download <filename> <root>")
    }

    filename := args[0]
    root := args[1]

    ctx := context.Background()

    logrus.SetOutput(os.Stderr)
    logrus.SetLevel(logrus.DebugLevel)

    indexerClient, err := indexer.NewClient("https://rpc-storage-testnet-turbo.0g.ai", indexer.IndexerClientOption{
        LogOption: zg_common.LogOption{Logger: logrus.StandardLogger()},
    })
    if err != nil {
        return fmt.Errorf("Failed to create indexer client: %v", err)
    }

    if err := indexerClient.Download(ctx, root, filename, false); err != nil {
        return fmt.Errorf("Download failed: %v", err)
    }

    fmt.Println("Download successful.")
    return nil
}